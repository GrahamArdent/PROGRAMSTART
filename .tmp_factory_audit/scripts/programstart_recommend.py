from __future__ import annotations

# ruff: noqa: I001

import argparse
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

try:
    from .programstart_common import load_registry, warn_direct_script_invocation, workspace_path
    from .programstart_context import load_knowledge_base
except ImportError:  # pragma: no cover - standalone script execution fallback
    from programstart_common import load_registry, warn_direct_script_invocation, workspace_path  # type: ignore
    from programstart_context import load_knowledge_base  # type: ignore


@dataclass(slots=True)
class ProjectRecommendation:
    product_shape: str
    variant: str
    attach_userjourney: bool
    archetype: str
    stack_names: list[str] = field(default_factory=list)
    rationale: list[str] = field(default_factory=list)
    kickoff_files: list[str] = field(default_factory=list)
    next_commands: list[str] = field(default_factory=list)


def parse_kickoff_inputs(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    values: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if ":" not in line:
            continue
        key, raw = line.split(":", 1)
        key = key.strip()
        if key.isupper():
            values[key] = raw.strip()
    return values


def normalize_shape(value: str | None) -> str:
    if not value:
        return "other"
    return value.strip().lower()


def infer_variant(product_shape: str, needs: set[str], regulated: bool) -> str:
    if regulated or {"audit", "regulated", "multi-team"} & needs:
        return "enterprise"
    if product_shape in {"cli tool", "library"} and not ({"agents", "rag", "durable-workflows"} & needs):
        return "lite"
    return "product"


def stack_exists(knowledge_base: dict[str, Any], stack_name: str) -> bool:
    return any(item.get("name", "").lower() == stack_name.lower() for item in knowledge_base.get("stacks", []))


def choose_stack_names(product_shape: str, needs: set[str], knowledge_base: dict[str, Any]) -> tuple[str, list[str], list[str]]:
    stacks: list[str] = []
    rationale: list[str] = []
    archetype = "General product planning workflow"

    if product_shape == "cli tool":
        archetype = "Type-safe CLI planning toolkit"
        stacks.extend(["Pydantic", "pytest", "Hypothesis", "Ruff", "uv"])
        rationale.extend(
            [
                "CLI tools benefit from strong boundary validation and predictable local execution.",
                "Property-based testing is especially effective for parser and scoring logic.",
            ]
        )
    elif product_shape == "api service":
        archetype = "Typed API and automation platform"
        stacks.extend(["FastAPI", "PostgreSQL", "Pydantic", "OpenTelemetry", "pytest"])
        rationale.extend(
            [
                "Typed APIs need explicit validation and contract discipline.",
                "Operational visibility matters early for service-oriented delivery.",
            ]
        )
    elif product_shape in {"web app", "mobile app"}:
        archetype = "Interactive product workflow"
        stacks.extend(["Next.js", "PostgreSQL", "Playwright", "Pydantic"])
        rationale.append("Interactive products need route, state, and acceptance discipline from the start.")
    elif product_shape == "data pipeline":
        archetype = "Data and automation workflow"
        stacks.extend(["FastAPI", "DuckDB", "Polars", "Pydantic"])
        rationale.append("Pipelines need operator-safe contracts and analytical tooling, not UI-first assumptions.")
    else:
        archetype = "Balanced production workflow"
        stacks.extend(["Pydantic", "pytest", "Ruff", "uv"])
        rationale.append("A balanced default is safer until the product shape is clarified.")

    if {"rag", "llm", "ai"} & needs:
        stacks.extend(["LiteLLM", "Instructor"])
        rationale.append("LLM-enabled products should centralize provider routing and validate every model output.")
    if {"vector", "semantic-search", "rag"} & needs:
        stacks.append("ChromaDB")
        rationale.append("Hybrid retrieval is useful when lexical authority needs semantic augmentation.")
    if {"agents", "durable-workflows"} & needs:
        stacks.extend(["Temporal", "LangGraph"])
        rationale.append("Long-running or agentic flows need durable orchestration instead of ad hoc retries.")

    deduped = [name for i, name in enumerate(stacks) if name not in stacks[:i] and stack_exists(knowledge_base, name)]
    return archetype, deduped, rationale


def build_recommendation(
    *,
    product_shape: str,
    needs: set[str],
    regulated: bool,
    attach_userjourney: bool | None,
) -> ProjectRecommendation:
    registry = load_registry()
    knowledge_base = load_knowledge_base()
    variant = infer_variant(product_shape, needs, regulated)
    should_attach = attach_userjourney if attach_userjourney is not None else product_shape in {"web app", "mobile app"}
    archetype, stack_names, rationale = choose_stack_names(product_shape, needs, knowledge_base)

    kickoff_files = list(registry.get("workflow_guidance", {}).get("kickoff", {}).get("files", []))
    next_commands = [
        f"programstart init --dest <folder> --project-name <name> --variant {variant} --product-shape \"{product_shape}\"",
        "programstart validate --check bootstrap-assets",
        "programstart next",
        "programstart guide --system programbuild",
    ]
    if should_attach:
        next_commands.insert(1, "programstart attach userjourney --source <path-to-userjourney-template>")

    if should_attach:
        rationale.append("The product shape implies real end-user onboarding or activation design work.")

    return ProjectRecommendation(
        product_shape=product_shape,
        variant=variant,
        attach_userjourney=should_attach,
        archetype=archetype,
        stack_names=stack_names,
        rationale=rationale,
        kickoff_files=kickoff_files,
        next_commands=next_commands,
    )


def load_recommendation_inputs(args: argparse.Namespace) -> tuple[str, set[str]]:
    kickoff_values = parse_kickoff_inputs(workspace_path("PROGRAMBUILD/PROGRAMBUILD_KICKOFF_PACKET.md"))
    product_shape = normalize_shape(args.product_shape or kickoff_values.get("PRODUCT_SHAPE"))
    needs = {item.strip().lower() for item in (args.need or []) if item.strip()}
    inferred_text = " ".join(
        value
        for key, value in kickoff_values.items()
        if key in {"CORE_PROBLEM", "ONE_LINE_DESCRIPTION", "KNOWN_CONSTRAINTS"}
    ).lower()
    if "ai" in inferred_text:
        needs.add("ai")
    if "rag" in inferred_text:
        needs.add("rag")
    if "agent" in inferred_text:
        needs.add("agents")
    return product_shape, needs


def print_recommendation(recommendation: ProjectRecommendation) -> None:
    print("PROGRAMSTART Recommendation")
    print(f"- product shape: {recommendation.product_shape}")
    print(f"- variant: {recommendation.variant}")
    print(f"- attach USERJOURNEY: {'yes' if recommendation.attach_userjourney else 'no'}")
    print(f"- archetype: {recommendation.archetype}")
    suggested_stacks = (
        ", ".join(recommendation.stack_names)
        if recommendation.stack_names
        else "none matched current KB"
    )
    print(f"- suggested stacks: {suggested_stacks}")
    print("- rationale:")
    for item in recommendation.rationale:
        print(f"  - {item}")
    print("- kickoff files:")
    for item in recommendation.kickoff_files:
        print(f"  - {item}")
    print("- next commands:")
    for item in recommendation.next_commands:
        print(f"  - {item}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Recommend the right PROGRAMSTART project setup and stack profile."
    )
    parser.add_argument(
        "--product-shape",
        help="Product shape, for example 'web app', 'CLI tool', or 'API service'.",
    )
    parser.add_argument(
        "--need",
        action="append",
        help="Repeated capability need, for example --need rag --need durable-workflows.",
    )
    parser.add_argument(
        "--regulated",
        action="store_true",
        help="Recommend stronger governance for regulated or high-consequence work.",
    )
    parser.add_argument(
        "--attach-userjourney",
        dest="attach_userjourney",
        action="store_true",
        help="Force USERJOURNEY attachment.",
    )
    parser.add_argument(
        "--no-attach-userjourney",
        dest="attach_userjourney",
        action="store_false",
        help="Force PROGRAMBUILD-only flow.",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of text.")
    parser.set_defaults(attach_userjourney=None)
    args = parser.parse_args(argv)

    product_shape, needs = load_recommendation_inputs(args)
    recommendation = build_recommendation(
        product_shape=product_shape,
        needs=needs,
        regulated=args.regulated,
        attach_userjourney=args.attach_userjourney,
    )

    if args.json:
        print(json.dumps(asdict(recommendation), indent=2))
    else:
        print_recommendation(recommendation)
    return 0


if __name__ == "__main__":  # pragma: no cover
    warn_direct_script_invocation("'uv run programstart recommend' or 'pb recommend'")
    raise SystemExit(main())
