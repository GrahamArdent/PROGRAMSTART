from __future__ import annotations

# ruff: noqa: I001

import argparse
import json
import re
from dataclasses import asdict, dataclass, field
from datetime import datetime, UTC
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
    service_names: list[str] = field(default_factory=list)
    cli_tool_names: list[str] = field(default_factory=list)
    api_names: list[str] = field(default_factory=list)
    rationale: list[str] = field(default_factory=list)
    service_notes: list[str] = field(default_factory=list)
    cli_notes: list[str] = field(default_factory=list)
    api_notes: list[str] = field(default_factory=list)
    kickoff_files: list[str] = field(default_factory=list)
    next_commands: list[str] = field(default_factory=list)
    prompt_principles: list[str] = field(default_factory=list)
    prompt_patterns: list[str] = field(default_factory=list)
    prompt_anti_patterns: list[str] = field(default_factory=list)
    matched_domains: list[str] = field(default_factory=list)
    coverage_warnings: list[dict[str, str]] = field(default_factory=list)
    stack_evidence: list[dict[str, object]] = field(default_factory=list)
    service_evidence: list[dict[str, object]] = field(default_factory=list)
    api_evidence: list[dict[str, object]] = field(default_factory=list)
    cli_evidence: list[dict[str, object]] = field(default_factory=list)
    rule_evidence: list[dict[str, str]] = field(default_factory=list)
    actionability_summary: list[dict[str, str]] = field(default_factory=list)
    alternatives: list[dict[str, str]] = field(default_factory=list)
    confidence: str = "medium"
    generated_prompt: str = ""
    prompt_generated_at: str = ""


TOKEN_SPLIT_RE = re.compile(r"[^a-z0-9]+")
CAPABILITY_ALIASES: dict[str, set[str]] = {
    "ai": {"ai", "llm", "language model"},
    "rag": {"rag", "retrieval", "semantic search", "semantic-search", "vector"},
    "agents": {"agents", "agent", "tool use", "tool-use", "mcp", "tool server", "tool-server"},
    "ml": {
        "ml",
        "machine learning",
        "machine-learning",
        "training",
        "fine-tuning",
        "fine tuning",
        "experiment tracking",
        "experiment-tracking",
    },
    "durable-workflows": {"durable workflows", "durable-workflows", "workflow", "orchestration"},
    "authentication": {"authentication", "auth", "login", "mobile auth", "mobile-auth"},
    "authorization": {"authorization", "rbac", "permissions"},
    "sso": {"sso", "single sign on", "single-sign-on", "scim", "enterprise auth", "enterprise-auth"},
    "compliance": {"compliance", "audit", "audit readiness", "security program", "regulated"},
    "observability": {"observability", "monitoring", "tracing", "metrics", "logging"},
    "realtime": {"realtime", "real time", "pubsub", "presence", "collaboration", "websockets"},
    "subscriptions": {"subscriptions", "subscription", "billing", "in app purchases", "in-app-purchases", "entitlements"},
    "payments": {"payments", "checkout", "payment processing", "payment-processing", "stripe"},
    "email": {"email", "email delivery", "email-delivery", "transactional email", "transactional-email"},
    "customer-data": {"customer data", "customer-data", "crm", "support", "analytics routing"},
    "shipping": {"shipping", "fulfillment", "labels", "logistics"},
    "tax": {"tax", "sales tax", "sales-tax", "vat"},
    "cloud": {"cloud", "hosting", "deploy", "deployment", "infrastructure", "serverless"},
    "database": {"database", "postgres", "sql", "storage"},
    "testing": {"testing", "test automation", "test-automation", "e2e testing", "e2e-testing"},
    "monorepo": {"monorepo", "multi package", "multi-package", "build graph", "build-graph"},
    "python": {"python", "automation"},
    "javascript": {"javascript", "typescript", "frontend"},
    "mobile": {"mobile", "ios", "android", "push notifications", "push-notifications"},
    "desktop": {"desktop", "local first", "local-first", "offline"},
}


def normalize_text(value: str) -> str:
    return TOKEN_SPLIT_RE.sub(" ", value.strip().lower()).strip()


def tokenize_text(value: str) -> set[str]:
    normalized = normalize_text(value)
    return {token for token in normalized.split() if token}


def expand_capability_terms(values: set[str]) -> set[str]:
    expanded: set[str] = set()
    normalized_values = {normalize_text(value) for value in values if normalize_text(value)}
    for value in normalized_values:
        expanded.add(value)
        for canonical, aliases in CAPABILITY_ALIASES.items():
            normalized_aliases = {normalize_text(alias) for alias in aliases}
            if value == canonical or value in normalized_aliases:
                expanded.add(canonical)
                expanded |= normalized_aliases
    return expanded


def normalized_trigger_set(values: list[str]) -> set[str]:
    return {normalize_text(value) for value in values if normalize_text(value)}


def matching_decision_rules(
    *,
    product_shape: str,
    needs: set[str],
    matched_domains: list[str],
    knowledge_base: dict[str, Any],
) -> list[dict[str, Any]]:
    normalized_shape = normalize_text(product_shape)
    normalized_needs = expand_capability_terms(needs)
    normalized_domains = {normalize_text(item) for item in matched_domains}
    matched_rules: list[dict[str, Any]] = []
    for rule in knowledge_base.get("decision_rules", []):
        rule_shapes = normalized_trigger_set(rule.get("match_product_shapes", []))
        rule_needs = normalized_trigger_set(rule.get("match_needs", []))
        rule_domains = normalized_trigger_set(rule.get("match_domains", []))
        if rule_shapes and normalized_shape not in rule_shapes:
            continue
        if rule_needs and not (rule_needs & normalized_needs):
            continue
        if rule_domains and not (rule_domains & normalized_domains):
            continue
        if rule_shapes or rule_needs or rule_domains:
            matched_rules.append(rule)
    return matched_rules


def classify_actionability(*, category: str, entry: dict[str, Any]) -> str:
    if category == "service":
        return "automation-supported" if entry.get("automation_supported") else "manual-setup"
    if category in {"api", "cli"}:
        return "manual-setup"
    return "advice-only"


def build_actionability_summary(
    *,
    stack_evidence: list[dict[str, object]],
    service_names: list[str],
    api_names: list[str],
    cli_names: list[str],
    knowledge_base: dict[str, Any],
) -> list[dict[str, str]]:
    summary: list[dict[str, str]] = []
    for item in stack_evidence[:5]:
        summary.append(
            {
                "name": str(item.get("name", "")),
                "category": "stack",
                "actionability": "advice-only",
                "reason": "Stack selection informs architecture and scaffolding but is not directly provisioned.",
            }
        )

    def add_entries(names: list[str], entries: list[dict[str, Any]], category: str, reason_key: str) -> None:
        for name in names:
            entry = next((item for item in entries if str(item.get("name", "")) == name), None)
            if not entry:
                continue
            reason = {
                "service": "Provisioning support depends on provider automation coverage.",
                "api": "API templates require env wiring and product-specific integration work.",
                "cli": "CLI installation and authentication remain explicit setup steps.",
            }[reason_key]
            summary.append(
                {
                    "name": name,
                    "category": category,
                    "actionability": classify_actionability(category=reason_key, entry=entry),
                    "reason": reason,
                }
            )

    add_entries(service_names, knowledge_base.get("provisioning_services", []), "service", "service")
    add_entries(api_names, knowledge_base.get("third_party_apis", []), "api", "api")
    add_entries(cli_names, knowledge_base.get("cli_tools", []), "cli", "cli")
    return summary


def stack_entry_text(entry: dict[str, Any]) -> str:
    parts: list[str] = [
        str(entry.get("name", "")),
        str(entry.get("layer", "")),
        " ".join(entry.get("aliases", [])),
        " ".join(entry.get("delivery_models", [])),
        " ".join(entry.get("strengths", [])),
        " ".join(entry.get("tradeoffs", [])),
        " ".join(entry.get("best_for", [])),
        " ".join(entry.get("avoid_when", [])),
        " ".join(entry.get("capabilities", [])),
        " ".join(entry.get("risks", [])),
        " ".join(entry.get("best_practices", [])),
    ]
    return normalize_text(" ".join(parts))


def stack_risk_text(entry: dict[str, Any]) -> str:
    parts = [" ".join(entry.get("tradeoffs", [])), " ".join(entry.get("avoid_when", [])), " ".join(entry.get("risks", []))]
    return normalize_text(" ".join(parts))


def matching_integration_patterns(
    *,
    product_shape: str,
    needs: set[str],
    knowledge_base: dict[str, Any],
) -> dict[str, list[str]]:
    """Return a map of stack name (lowered) -> list of pattern names that matched."""
    normalized_needs = expand_capability_terms(needs)
    pattern_boosts: dict[str, list[str]] = {}
    for pattern in knowledge_base.get("integration_patterns", []):
        fit_for_text = normalize_text(" ".join(pattern.get("fit_for", [])))
        pattern_name = str(pattern.get("name", ""))
        matched = False
        for need in normalized_needs:
            if need and need in fit_for_text:
                matched = True
                break
        if not matched and normalize_text(product_shape) in fit_for_text:
            matched = True
        if not matched:
            continue
        for component in pattern.get("components", []):
            key = component.lower()
            if key not in pattern_boosts:
                pattern_boosts[key] = []
            pattern_boosts[key].append(pattern_name)
    return pattern_boosts


def shape_profile(product_shape: str) -> tuple[str, list[str], set[str], list[str]]:
    if product_shape == "cli tool":
        return (
            "Type-safe CLI planning toolkit",
            ["Pydantic", "pytest", "Hypothesis", "Ruff", "uv"],
            {"cli", "validation", "testing", "automation", "developer tooling"},
            ["Developer experience, quality, and supply chain"],
        )
    if product_shape == "api service":
        return (
            "Typed API and automation platform",
            ["FastAPI", "PostgreSQL", "Pydantic", "OpenTelemetry", "pytest"],
            {"api contracts", "automation", "service observability", "validation", "async io"},
            ["API, workflow, and backend platforms", "Cloud, infrastructure, and platform operations"],
        )
    if product_shape == "web app":
        return (
            "Interactive product workflow",
            ["Next.js", "PostgreSQL", "Playwright", "Pydantic"],
            {"ssr", "route driven rendering", "browser testing", "authentication", "interactive client state"},
            ["Web and frontend product delivery", "Cloud, infrastructure, and platform operations"],
        )
    if product_shape == "mobile app":
        return (
            "Mobile product workflow",
            ["React Native", "Expo", "Firebase", "Pydantic"],
            {"ios", "android", "shared ui", "mobile auth", "push notifications", "in app purchases"},
            ["Mobile and cross-platform apps", "Web and frontend product delivery"],
        )
    if product_shape == "data pipeline":
        return (
            "Data and automation workflow",
            ["FastAPI", "DuckDB", "Polars", "Pydantic"],
            {"etl", "analytics sql", "columnar processing", "feature pipelines", "automation"},
            ["Data engineering and analytics", "API, workflow, and backend platforms"],
        )
    return (
        "Balanced production workflow",
        ["Pydantic", "pytest", "Ruff", "uv"],
        {"validation", "testing", "automation"},
        ["Developer experience, quality, and supply chain"],
    )


def infer_domain_names(product_shape: str, needs: set[str], regulated: bool, knowledge_base: dict[str, Any]) -> list[str]:
    _, _, _, base_domains = shape_profile(product_shape)
    ordered_names: list[str] = []

    def add_domain(name: str) -> None:
        if name in ordered_names:
            return
        if any(item.get("name", "") == name for item in knowledge_base.get("coverage_domains", [])):
            ordered_names.append(name)

    for item in base_domains:
        add_domain(item)

    domain_map: dict[str, str] = {}
    for canonical, aliases in CAPABILITY_ALIASES.items():
        _need_to_domain: dict[str, str] = {
            "ai": "AI, retrieval, and agent systems",
            "rag": "AI, retrieval, and agent systems",
            "agents": "AI, retrieval, and agent systems",
            "ml": "AI, retrieval, and agent systems",
            "durable-workflows": "API, workflow, and backend platforms",
            "realtime": "Realtime collaboration, messaging, and eventing",
            "subscriptions": "Commerce, communication, and product integrations",
            "payments": "Commerce, communication, and product integrations",
            "email": "Commerce, communication, and product integrations",
            "customer-data": "Commerce, communication, and product integrations",
            "shipping": "Commerce, communication, and product integrations",
            "tax": "Commerce, communication, and product integrations",
            "authentication": "Identity, security, and regulated delivery",
            "authorization": "Identity, security, and regulated delivery",
            "sso": "Identity, security, and regulated delivery",
            "compliance": "Identity, security, and regulated delivery",
            "observability": "Cloud, infrastructure, and platform operations",
            "cloud": "Cloud, infrastructure, and platform operations",
            "database": "Cloud, infrastructure, and platform operations",
            "desktop": "Desktop, local-first, and offline-capable software",
            "testing": "Developer experience, quality, and supply chain",
            "monorepo": "Developer experience, quality, and supply chain",
            "python": "Developer experience, quality, and supply chain",
            "javascript": "Web and frontend product delivery",
            "mobile": "Mobile and cross-platform apps",
        }
        target_domain = _need_to_domain.get(canonical)
        if target_domain:
            domain_map[canonical] = target_domain
            for alias in aliases:
                domain_map[normalize_text(alias)] = target_domain
    for need in sorted(expand_capability_terms(needs)):
        mapped = domain_map.get(need)
        if mapped:
            add_domain(mapped)

    if regulated:
        add_domain("Identity, security, and regulated delivery")

    return ordered_names


def merge_unique_names(names: list[str]) -> list[str]:
    ordered: list[str] = []
    seen: set[str] = set()
    for name in names:
        normalized = normalize_text(name)
        if not normalized or normalized in seen:
            continue
        ordered.append(name)
        seen.add(normalized)
    return ordered


def preferred_rule_items_for_layer(
    *,
    rules: list[dict[str, Any]],
    knowledge_base: dict[str, Any],
    layer: str,
) -> list[str]:
    kb_key = {
        "stacks": "stacks",
        "provisioning_services": "provisioning_services",
        "third_party_apis": "third_party_apis",
        "cli_tools": "cli_tools",
    }.get(layer, "")
    valid_names = {
        normalize_text(str(item.get("name", ""))) for item in knowledge_base.get(kb_key, []) if str(item.get("name", "")).strip()
    }
    preferred: list[str] = []
    for rule in rules:
        target_layers = normalized_trigger_set(rule.get("target_layers", []))
        if target_layers and layer not in target_layers:
            continue
        for item in rule.get("prefer_items", []):
            if normalize_text(item) in valid_names:
                preferred.append(str(item))
    return merge_unique_names(preferred)


def actionability_follow_up_commands(actionability_summary: list[dict[str, str]]) -> list[str]:
    commands: list[str] = []
    if any(item.get("actionability") == "advice-only" for item in actionability_summary):
        commands.append(
            "Review outputs/factory/create-plan.md to confirm stack, rule, and architecture guidance before implementation"
        )
    if any(item.get("actionability") == "automation-supported" for item in actionability_summary):
        commands.append(
            "Review outputs/factory/provisioning-plan.md and execute automation-supported provisioning before manual setup"
        )
    if any(item.get("actionability") == "manual-setup" for item in actionability_summary):
        commands.append("Use outputs/factory/setup-surface.md to complete manual CLI installs, auth steps, and API env wiring")
    return commands


def comparison_bonus(
    *,
    item_name: str,
    selected_stacks: set[str],
    needs: set[str],
    comparisons: list[dict[str, Any]],
) -> tuple[int, list[str], list[dict[str, str]]]:
    bonus = 0
    reasons: list[str] = []
    alternatives: list[dict[str, str]] = []
    normalized_item = item_name.lower()
    normalized_needs = expand_capability_terms(needs)
    normalized_stacks = {item.lower() for item in selected_stacks}
    for comparison in comparisons:
        related_items = {normalize_text(item) for item in comparison.get("related_items", [])}
        compared_versions = {normalize_text(item) for item in comparison.get("compared_versions", [])}
        if normalized_item not in related_items and normalized_item not in compared_versions:
            continue
        if not (related_items & normalized_stacks or related_items & normalized_needs or compared_versions & normalized_needs):
            continue
        decision = str(comparison.get("decision", ""))
        summary = str(comparison.get("summary", ""))
        if normalized_item in normalize_text(decision):
            bonus += 3
            reasons.append(decision)
        else:
            bonus += 1
            reasons.append(summary)
        alternatives.append(
            {
                "item": str(comparison.get("name", "")),
                "category": "comparison",
                "rationale": decision or summary,
            }
        )
    return bonus, reasons, alternatives


def select_triggered_entries(
    *,
    entries: list[dict[str, Any]],
    product_shape: str,
    needs: set[str],
    stack_names: list[str],
    service_names: list[str] | None = None,
    api_names: list[str] | None = None,
    comparisons: list[dict[str, Any]] | None = None,
    decision_rules: list[dict[str, Any]] | None = None,
    matched_domains: list[str] | None = None,
    category: str = "",
    min_score: int = 4,
) -> tuple[list[str], list[str], list[dict[str, object]], list[dict[str, str]]]:
    selected_names: list[str] = []
    notes: list[str] = []
    evidence: list[dict[str, object]] = []
    alternatives: list[dict[str, str]] = []
    normalized_shape = normalize_text(product_shape)
    normalized_needs = expand_capability_terms(needs)
    normalized_stacks = {normalize_text(item) for item in stack_names}
    normalized_services = {normalize_text(item) for item in (service_names or [])}
    normalized_apis = {normalize_text(item) for item in (api_names or [])}
    comparisons = comparisons or []
    applicable_rules = matching_decision_rules(
        product_shape=product_shape,
        needs=needs,
        matched_domains=matched_domains or [],
        knowledge_base={"decision_rules": decision_rules or []},
    )

    candidates: list[dict[str, object]] = []
    for item in entries:
        name = str(item.get("name", "")).strip()
        if not name:
            continue
        score = 0
        reasons: list[str] = []
        trigger_shapes = normalized_trigger_set(item.get("trigger_shapes", []))
        trigger_needs = normalized_trigger_set(item.get("trigger_needs", []))
        trigger_stacks = normalized_trigger_set(item.get("trigger_stacks", []))
        trigger_services = normalized_trigger_set(item.get("trigger_services", []))
        trigger_apis = normalized_trigger_set(item.get("trigger_apis", []))
        need_matches = sorted(trigger_needs & normalized_needs)
        stack_matches = sorted(trigger_stacks & normalized_stacks)
        service_matches = sorted(trigger_services & normalized_services)
        api_matches = sorted(trigger_apis & normalized_apis)
        rule_preferred = False
        rule_cautioned = False

        if normalized_shape in trigger_shapes:
            score += 5
            reasons.append(f"Matches product shape {product_shape}.")
        if need_matches:
            score += min(6, len(need_matches) * 2)
            reasons.append(f"Matches capability triggers: {', '.join(need_matches[:4])}.")
        if stack_matches:
            score += min(6, len(stack_matches) * 2)
            reasons.append(f"Matches recommended stacks: {', '.join(stack_matches[:3])}.")
        if service_matches:
            score += min(4, len(service_matches) * 2)
            reasons.append(f"Complements inferred services: {', '.join(service_matches[:3])}.")
        if api_matches:
            score += min(4, len(api_matches) * 2)
            reasons.append(f"Complements inferred APIs: {', '.join(api_matches[:3])}.")

        normalized_name = normalize_text(name)
        for rule in applicable_rules:
            target_layers = normalized_trigger_set(rule.get("target_layers", []))
            if target_layers and category and category not in target_layers:
                continue
            if normalized_name in normalized_trigger_set(rule.get("prefer_items", [])):
                score += 4
                rule_preferred = True
                reasons.append(f"KB rule preference: {rule.get('title', '')}.")
            if normalized_name in normalized_trigger_set(rule.get("avoid_items", [])):
                score -= 3
                rule_cautioned = True
                reasons.append(f"KB rule caution: {rule.get('title', '')}.")

        if category == "third_party_apis" and not (need_matches or service_matches or api_matches or rule_preferred):
            continue

        if category == "third_party_apis" and rule_cautioned and not (need_matches or rule_preferred):
            continue

        bonus, comparison_reasons, comparison_alts = comparison_bonus(
            item_name=name,
            selected_stacks=normalized_stacks,
            needs=normalized_needs,
            comparisons=comparisons,
        )
        if bonus:
            score += bonus
            reasons.extend(comparison_reasons[:2])
            alternatives.extend(comparison_alts)

        if score < min_score:
            continue

        candidates.append({"name": name, "score": score, "reasons": reasons})

    ordered_candidates = sorted(candidates, key=lambda item: (-int(item["score"]), str(item["name"]).lower()))
    for candidate in ordered_candidates:
        name = str(candidate["name"])
        if name in selected_names:
            continue
        selected_names.append(name)
        evidence.append({"name": name, "score": int(candidate["score"]), "reasons": list(candidate.get("reasons", []))[:4]})
        entry = next((entry for entry in entries if str(entry.get("name", "")).strip() == name), None)
        if entry:
            for note in entry.get("notes", []):
                if note not in notes:
                    notes.append(note)

    return selected_names, notes, evidence, alternatives


def build_stack_candidates(
    product_shape: str,
    needs: set[str],
    regulated: bool,
    knowledge_base: dict[str, Any],
) -> tuple[
    str, list[str], list[dict[str, object]], list[str], list[dict[str, str]], list[dict[str, str]], list[dict[str, str]], str
]:
    archetype, baseline_stacks, intent_terms, matched_domain_names = shape_profile(product_shape)
    selected_domain_names = infer_domain_names(product_shape, needs, regulated, knowledge_base)
    selected_domains = [
        item for item in knowledge_base.get("coverage_domains", []) if item.get("name", "") in selected_domain_names
    ]
    intent_terms = {normalize_text(item) for item in intent_terms | set(needs) if normalize_text(item)}
    applicable_rules = matching_decision_rules(
        product_shape=product_shape,
        needs=needs,
        matched_domains=[item.get("name", "") for item in selected_domains],
        knowledge_base=knowledge_base,
    )
    rule_evidence = [
        {
            "title": str(rule.get("title", "")),
            "because": str(rule.get("because", "")),
            "confidence": str(rule.get("confidence", "medium")),
        }
        for rule in applicable_rules
    ]
    preferred_stack_names = merge_unique_names(
        baseline_stacks + preferred_rule_items_for_layer(rules=applicable_rules, knowledge_base=knowledge_base, layer="stacks")
    )
    preferred_lookup = {item.lower() for item in preferred_stack_names}

    comparisons = knowledge_base.get("comparisons", [])
    relations = knowledge_base.get("relationships", [])
    pattern_boosts = matching_integration_patterns(
        product_shape=product_shape,
        needs=needs,
        knowledge_base=knowledge_base,
    )
    candidates: list[dict[str, object]] = []

    for entry in knowledge_base.get("stacks", []):
        name = str(entry.get("name", "")).strip()
        if not name:
            continue
        score = 0
        reasons: list[str] = []
        supporting_domains: list[str] = []
        matched_terms: list[str] = []
        normalized_name = name.lower()
        text_blob = stack_entry_text(entry)
        risk_blob = stack_risk_text(entry)

        if normalized_name in preferred_lookup:
            score += 12
            reasons.append(f"Baseline fit for {product_shape}.")

        for domain in selected_domains:
            representative = {item.lower() for item in domain.get("representative_tools", [])}
            if normalized_name in representative:
                status = str(domain.get("status", ""))
                domain_score = {"strong": 8, "partial": 6, "seed": 4}.get(status, 5)
                score += domain_score
                supporting_domains.append(str(domain.get("name", "")))
                reasons.append(f"Representative tool for {domain.get('name', '')} ({status or 'unknown'} coverage).")

        matched_patterns = pattern_boosts.get(normalized_name, [])
        if matched_patterns:
            score += min(6, len(matched_patterns) * 3)
            reasons.append(f"Matches integration patterns: {', '.join(matched_patterns[:2])}.")

        for term in sorted(intent_terms):
            if term and term in text_blob:
                matched_terms.append(term)

        if matched_terms:
            score += min(10, len(matched_terms) * 2)
            reasons.append(f"Matches intent terms: {', '.join(matched_terms[:4])}.")

        if regulated and any(
            token in text_blob for token in ("security", "audit", "validation", "auth", "observability", "compliance")
        ):
            score += 3
            reasons.append("Improves governance, validation, or observability for regulated work.")

        for rule in applicable_rules:
            target_layers = normalized_trigger_set(rule.get("target_layers", []))
            if target_layers and "stacks" not in target_layers:
                continue
            if normalized_name in normalized_trigger_set(rule.get("prefer_items", [])):
                score += 4
                reasons.append(f"KB rule preference: {rule.get('title', '')}.")
            if normalized_name in normalized_trigger_set(rule.get("avoid_items", [])):
                score -= 3
                reasons.append(f"KB rule caution: {rule.get('title', '')}.")

        cautions = [term for term in matched_terms if term in risk_blob]
        if cautions:
            score -= min(4, len(cautions))
            reasons.append(f"Has tradeoffs near this problem shape: {', '.join(cautions[:3])}.")

        if score <= 0:
            continue

        candidates.append(
            {
                "name": name,
                "score": score,
                "reasons": reasons,
                "matched_terms": matched_terms,
                "supporting_domains": supporting_domains,
            }
        )

    candidate_lookup = {str(item["name"]): item for item in candidates}
    for relation in relations:
        if relation.get("relation") != "complements":
            continue
        subject = str(relation.get("subject", ""))
        obj = str(relation.get("object", ""))
        if subject in candidate_lookup and obj in candidate_lookup:
            if subject.lower() in preferred_lookup:
                candidate_lookup[obj]["score"] = int(candidate_lookup[obj]["score"]) + 2
                candidate_lookup[obj]["reasons"].append(f"Complements {subject} in KB relationships.")
            if obj.lower() in preferred_lookup:
                candidate_lookup[subject]["score"] = int(candidate_lookup[subject]["score"]) + 2
                candidate_lookup[subject]["reasons"].append(f"Complements {obj} in KB relationships.")

    ordered_candidates = sorted(
        candidates,
        key=lambda item: (-int(item["score"]), str(item["name"]).lower()),
    )

    selected_stack_names: list[str] = []
    for name in preferred_stack_names:
        if name in candidate_lookup and name not in selected_stack_names:
            selected_stack_names.append(name)

    additional_budget = 2 + max(0, len(preferred_stack_names) - len(baseline_stacks))
    for candidate in ordered_candidates:
        name = str(candidate["name"])
        if name in selected_stack_names:
            continue
        if len(selected_stack_names) >= len(preferred_stack_names) + additional_budget:
            break
        selected_stack_names.append(name)

    stack_evidence: list[dict[str, object]] = []
    for name in selected_stack_names:
        candidate = candidate_lookup.get(name)
        if not candidate:
            continue
        evidence_reasons = list(candidate.get("reasons", []))
        related_decisions = [
            item.get("decision", "") for item in comparisons if name in item.get("related_items", []) and item.get("decision", "")
        ]
        if related_decisions:
            evidence_reasons.append(related_decisions[0])
        stack_evidence.append(
            {
                "name": name,
                "score": int(candidate["score"]),
                "supporting_domains": list(candidate.get("supporting_domains", [])),
                "reasons": evidence_reasons[:4],
            }
        )

    matched_domains = [item.get("name", "") for item in selected_domains]
    coverage_warnings = [
        {
            "domain": str(item.get("name", "")),
            "status": str(item.get("status", "")),
            "summary": str(item.get("summary", "")),
            "gaps": "; ".join(item.get("current_gaps", [])[:2]) or "No explicit gaps recorded.",
        }
        for item in selected_domains
        if item.get("status") in {"partial", "seed"}
    ]

    alternatives: list[dict[str, str]] = []
    for candidate in ordered_candidates:
        name = str(candidate["name"])
        if name in selected_stack_names:
            continue
        alternatives.append(
            {
                "item": name,
                "category": "stack",
                "rationale": "; ".join(candidate.get("reasons", [])[:2]) or "Relevant, but scored below the selected stack set.",
            }
        )
        if len(alternatives) >= 2:
            break
    for comparison in comparisons:
        related_items = {item.lower() for item in comparison.get("related_items", [])}
        selected_items = {item.lower() for item in [*selected_stack_names]}
        if not (related_items & selected_items or related_items & {item.lower() for item in needs}):
            continue
        alternatives.append(
            {
                "item": str(comparison.get("name", "")),
                "category": "comparison",
                "rationale": str(comparison.get("decision", "")) or str(comparison.get("summary", "")),
            }
        )
        if len(alternatives) >= 4:
            break

    if any(item["status"] == "seed" for item in coverage_warnings):
        confidence = "low"
    elif coverage_warnings:
        confidence = "medium"
    elif len(ordered_candidates) < 3:
        confidence = "medium"
    else:
        confidence = "high"

    if matched_domains:
        matched_domain_names = matched_domains

    return (
        archetype,
        selected_stack_names,
        stack_evidence,
        matched_domain_names,
        coverage_warnings,
        alternatives,
        rule_evidence,
        confidence,
    )


def build_generated_prompt(
    *,
    product_shape: str,
    variant: str,
    attach_userjourney: bool,
    kickoff_files: list[str],
    rationale: list[str],
    prompt_principles: list[str],
    prompt_patterns: list[str],
    prompt_anti_patterns: list[str],
    coverage_warnings: list[dict[str, str]],
    service_names: list[str],
    cli_tool_names: list[str],
    api_names: list[str],
) -> str:
    files_line = ", ".join(kickoff_files) if kickoff_files else "registry kickoff files"
    services_line = ", ".join(service_names) if service_names else "none inferred"
    cli_line = ", ".join(cli_tool_names) if cli_tool_names else "none inferred"
    apis_line = ", ".join(api_names) if api_names else "none inferred"
    coverage_lines = (
        "\n".join(f"- {item['domain']}: {item['gaps']}" for item in coverage_warnings[:4]) if coverage_warnings else "none"
    )
    sections = [
        "## Task\nCreate a new project kickoff plan from the current PROGRAMSTART workflow assets.",
        "## Reasoning Steps\n"
        "1. Identify which authority files govern the active stage and variant.\n"
        "2. Confirm the product shape, variant, and USERJOURNEY attachment decision.\n"
        "3. Map each recommended stack and service to a concrete kickoff action.\n"
        "4. Flag any coverage gaps that need resolution before locking.\n"
        "5. Produce the plan in the file structure required by the registry.",
        f"## Project Context\n"
        f"- Product shape: {product_shape}\n"
        f"- Variant: {variant}\n"
        f"- USERJOURNEY attached: {'yes' if attach_userjourney else 'no'}\n"
        f"- Authoritative files: {files_line}",
        f"## Infrastructure\n- Services: {services_line}\n- Setup CLIs: {cli_line}\n- API templates: {apis_line}",
        "## Decision Rationale\n" + "\n".join(f"- {r}" for r in rationale[:6]),
        "## Prompt Principles\n" + "\n".join(f"- {p}" for p in prompt_principles[:8]),
        "## Prompt Patterns\n" + "\n".join(f"- {p}" for p in prompt_patterns[:8]),
        "## Anti-Patterns\n"
        + "\n".join(
            f"- {p}"
            for p in (
                prompt_anti_patterns[:8] if prompt_anti_patterns else ["Do not invent unsupported files, rules, or citations."]
            )
        ),
        f"## Coverage Warnings\n{coverage_lines}",
        "## Constraints\n"
        "- Do not invent file lists or stage order outside the registry and authority docs.\n"
        "- Provision project-scoped services in the generated repo only.",
    ]
    return "\n\n".join(sections)


def normalize_prompt_guidance(prompt_guidance: dict[str, Any]) -> tuple[list[str], list[str], list[str]]:
    def clean_items(items: list[str]) -> list[str]:
        seen: set[str] = set()
        cleaned: list[str] = []
        for item in items:
            value = str(item).strip()
            if not value:
                continue
            key = value.lower()
            if key in seen:
                continue
            seen.add(key)
            cleaned.append(value)
        return cleaned

    principles = clean_items(
        [
            *list(prompt_guidance.get("principles", [])),
            str(prompt_guidance.get("output_contracts", "")),
            str(prompt_guidance.get("verification_loops", "")),
            str(prompt_guidance.get("completeness_contracts", "")),
        ]
    )
    patterns = clean_items(
        [
            *list(prompt_guidance.get("patterns", [])),
            str(prompt_guidance.get("tool_persistence", "")),
            str(prompt_guidance.get("research_mode", "")),
            str(prompt_guidance.get("reasoning_effort", "")),
            str(prompt_guidance.get("citation_rules", "")),
            str(prompt_guidance.get("empty_result_recovery", "")),
        ]
    )
    anti_patterns = clean_items(list(prompt_guidance.get("anti_patterns", [])))
    if not anti_patterns:
        anti_patterns = [
            "Do not invent unsupported files, rules, or citations.",
            "Do not skip verification or assume tool output is complete.",
            "Do not add features, stages, or documents outside the registry authority model.",
        ]
    return principles, patterns, anti_patterns


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
    if product_shape in {"cli tool", "library"} and not (
        {"agents", "rag", "durable-workflows", "ml", "training", "fine-tuning", "machine learning", "machine-learning"} & needs
    ):
        return "lite"
    return "product"


def stack_exists(knowledge_base: dict[str, Any], stack_name: str) -> bool:
    return any(item.get("name", "").lower() == stack_name.lower() for item in knowledge_base.get("stacks", []))


def choose_service_names(
    product_shape: str,
    needs: set[str],
    stack_names: list[str],
    matched_domains: list[str],
    knowledge_base: dict[str, Any],
) -> tuple[list[str], list[str], list[dict[str, object]], list[dict[str, str]]]:
    return select_triggered_entries(
        entries=knowledge_base.get("provisioning_services", []),
        product_shape=product_shape,
        needs=needs,
        stack_names=stack_names,
        comparisons=knowledge_base.get("comparisons", []),
        decision_rules=knowledge_base.get("decision_rules", []),
        matched_domains=matched_domains,
        category="provisioning_services",
        min_score=4,
    )


def choose_api_names(
    product_shape: str,
    needs: set[str],
    stack_names: list[str],
    matched_domains: list[str],
    knowledge_base: dict[str, Any],
) -> tuple[list[str], list[str], list[dict[str, object]], list[dict[str, str]]]:
    return select_triggered_entries(
        entries=knowledge_base.get("third_party_apis", []),
        product_shape=product_shape,
        needs=needs,
        stack_names=stack_names,
        comparisons=knowledge_base.get("comparisons", []),
        decision_rules=knowledge_base.get("decision_rules", []),
        matched_domains=matched_domains,
        category="third_party_apis",
        min_score=2,
    )


def choose_cli_tool_names(
    product_shape: str,
    needs: set[str],
    stack_names: list[str],
    service_names: list[str],
    api_names: list[str],
    matched_domains: list[str],
    knowledge_base: dict[str, Any],
) -> tuple[list[str], list[str], list[dict[str, object]], list[dict[str, str]]]:
    return select_triggered_entries(
        entries=knowledge_base.get("cli_tools", []),
        product_shape=product_shape,
        needs=needs,
        stack_names=stack_names,
        service_names=service_names,
        api_names=api_names,
        comparisons=knowledge_base.get("comparisons", []),
        decision_rules=knowledge_base.get("decision_rules", []),
        matched_domains=matched_domains,
        category="cli_tools",
        min_score=3,
    )


def build_recommendation(
    *,
    product_shape: str,
    needs: set[str],
    regulated: bool,
    attach_userjourney: bool | None,
) -> ProjectRecommendation:
    registry = load_registry()
    knowledge_base = load_knowledge_base()
    prompt_guidance = dict(knowledge_base.get("prompt_engineering_guidance", {}))
    normalized_needs = expand_capability_terms(needs)
    variant = infer_variant(product_shape, normalized_needs, regulated)
    should_attach = attach_userjourney if attach_userjourney is not None else product_shape in {"web app", "mobile app"}

    # #24: Detect needs that don't match any CAPABILITY_ALIASES canonical key
    recognized_canonical = set(CAPABILITY_ALIASES.keys())
    recognized_all = set()
    for aliases in CAPABILITY_ALIASES.values():
        recognized_all |= {normalize_text(a) for a in aliases}
    recognized_all |= recognized_canonical
    unrecognized_needs = sorted(n for n in needs if normalize_text(n) and normalize_text(n) not in recognized_all)

    archetype, stack_names, stack_evidence, matched_domains, coverage_warnings, alternatives, rule_evidence, confidence = (
        build_stack_candidates(
            product_shape,
            normalized_needs,
            regulated,
            knowledge_base,
        )
    )
    rationale = [
        f"Recommendation is scored from KB stack fit, coverage domains, and explicit relationships for {product_shape}.",
    ]
    if matched_domains:
        rationale.append(f"Most relevant KB domains: {', '.join(matched_domains)}.")
    if coverage_warnings:
        rationale.append("Some matched domains are not fully mature; review the coverage warnings before locking the stack.")
    if rule_evidence:
        rationale.append(f"KB decision rules applied: {', '.join(item['title'] for item in rule_evidence[:3])}.")
    top_stack_evidence = stack_evidence[:3]
    for item in top_stack_evidence:
        reasons = "; ".join(str(reason) for reason in item.get("reasons", [])[:2])
        rationale.append(f"{item.get('name')}: {reasons}")
    service_names, service_notes, service_evidence, service_alternatives = choose_service_names(
        product_shape,
        normalized_needs,
        stack_names,
        matched_domains,
        knowledge_base,
    )
    api_names, api_notes, api_evidence, api_alternatives = choose_api_names(
        product_shape,
        normalized_needs,
        stack_names,
        matched_domains,
        knowledge_base,
    )
    cli_tool_names, cli_notes, cli_evidence, cli_alternatives = choose_cli_tool_names(
        product_shape,
        normalized_needs,
        stack_names,
        service_names,
        api_names,
        matched_domains,
        knowledge_base,
    )
    actionability_summary = build_actionability_summary(
        stack_evidence=stack_evidence,
        service_names=service_names,
        api_names=api_names,
        cli_names=cli_tool_names,
        knowledge_base=knowledge_base,
    )
    combined_alternatives: list[dict[str, str]] = []
    for candidate in [*alternatives, *service_alternatives, *api_alternatives, *cli_alternatives]:
        key = (candidate.get("item", ""), candidate.get("category", ""))
        if any((item.get("item", ""), item.get("category", "")) == key for item in combined_alternatives):
            continue
        combined_alternatives.append(candidate)

    kickoff_files = list(registry.get("workflow_guidance", {}).get("kickoff", {}).get("files", []))
    next_commands = [f'programstart create --dest <folder> --project-name <name> --product-shape "{product_shape}"']
    if coverage_warnings:
        next_commands.append("Review coverage warnings in outputs/factory/create-plan.md before locking architecture")
    next_commands.extend(actionability_follow_up_commands(actionability_summary))
    if should_attach:
        next_commands.append("programstart attach userjourney --source <path-to-userjourney-template>")
    next_commands.extend(
        [
            f'programstart init --dest <folder> --project-name <name> --variant {variant} --product-shape "{product_shape}"',
            "programstart validate --check bootstrap-assets",
            "programstart next",
            "programstart guide --system programbuild",
        ]
    )

    if should_attach:
        rationale.append("The product shape implies real end-user onboarding or activation design work.")
    if unrecognized_needs:
        rationale.append(
            f"Unrecognized capability needs (not in KB aliases): {', '.join(unrecognized_needs)}. These were not factored into stack or service selection."
        )
    if service_evidence:
        rationale.append(f"Inferred services: {', '.join(str(item['name']) for item in service_evidence[:3])}.")
    if api_evidence:
        rationale.append(f"Inferred third-party APIs: {', '.join(str(item['name']) for item in api_evidence[:3])}.")

    prompt_principles, prompt_patterns, prompt_anti_patterns = normalize_prompt_guidance(prompt_guidance)
    generated_prompt = build_generated_prompt(
        product_shape=product_shape,
        variant=variant,
        attach_userjourney=should_attach,
        kickoff_files=kickoff_files,
        rationale=rationale,
        prompt_principles=prompt_principles,
        prompt_patterns=prompt_patterns,
        prompt_anti_patterns=prompt_anti_patterns,
        coverage_warnings=coverage_warnings,
        service_names=service_names,
        cli_tool_names=cli_tool_names,
        api_names=api_names,
    )

    return ProjectRecommendation(
        product_shape=product_shape,
        variant=variant,
        attach_userjourney=should_attach,
        archetype=archetype,
        stack_names=stack_names,
        service_names=service_names,
        cli_tool_names=cli_tool_names,
        api_names=api_names,
        rationale=rationale,
        service_notes=service_notes,
        cli_notes=cli_notes,
        api_notes=api_notes,
        kickoff_files=kickoff_files,
        next_commands=next_commands,
        prompt_principles=prompt_principles,
        prompt_patterns=prompt_patterns,
        prompt_anti_patterns=prompt_anti_patterns,
        matched_domains=matched_domains,
        coverage_warnings=coverage_warnings,
        stack_evidence=stack_evidence,
        service_evidence=service_evidence,
        api_evidence=api_evidence,
        cli_evidence=cli_evidence,
        rule_evidence=rule_evidence,
        actionability_summary=actionability_summary,
        alternatives=combined_alternatives,
        confidence=confidence,
        generated_prompt=generated_prompt,
        prompt_generated_at=datetime.now(UTC).isoformat(timespec="seconds"),
    )


def load_recommendation_inputs(args: argparse.Namespace) -> tuple[str, set[str]]:
    kickoff_values = parse_kickoff_inputs(workspace_path("PROGRAMBUILD/PROGRAMBUILD_KICKOFF_PACKET.md"))
    product_shape = normalize_shape(args.product_shape or kickoff_values.get("PRODUCT_SHAPE"))
    needs = {item.strip().lower() for item in (args.need or []) if item.strip()}
    inferred_text = " ".join(
        value for key, value in kickoff_values.items() if key in {"CORE_PROBLEM", "ONE_LINE_DESCRIPTION", "KNOWN_CONSTRAINTS"}
    ).lower()
    for canonical, aliases in CAPABILITY_ALIASES.items():
        if any(normalize_text(alias) in normalize_text(inferred_text) for alias in aliases):
            needs.add(canonical)
    return product_shape, expand_capability_terms(needs)


def re_evaluate_project(project_dir: str) -> dict[str, Any]:
    """Re-evaluate an existing project against the current PROGRAMSTART knowledge base.

    Reads the target project's kickoff inputs, re-runs the recommendation engine
    with the current (possibly updated) KB, and returns a comparison report
    showing what changed.
    """
    target = Path(project_dir).resolve()
    kickoff_path = target / "PROGRAMBUILD" / "PROGRAMBUILD_KICKOFF_PACKET.md"
    kickoff_values = parse_kickoff_inputs(kickoff_path)

    product_shape = normalize_shape(kickoff_values.get("PRODUCT_SHAPE"))
    needs: set[str] = set()
    inferred_text = " ".join(
        value for key, value in kickoff_values.items() if key in {"CORE_PROBLEM", "ONE_LINE_DESCRIPTION", "KNOWN_CONSTRAINTS"}
    ).lower()
    for canonical, aliases in CAPABILITY_ALIASES.items():
        if any(normalize_text(alias) in normalize_text(inferred_text) for alias in aliases):
            needs.add(canonical)
    needs = expand_capability_terms(needs)
    regulated = "regulated" in inferred_text or "compliance" in inferred_text

    current_rec = build_recommendation(
        product_shape=product_shape,
        needs=needs,
        regulated=regulated,
        attach_userjourney=None,
    )

    # Load the project's existing state for comparison
    target_registry_path = target / "config" / "process-registry.json"
    target_state: dict[str, Any] = {}
    if target_registry_path.exists():
        target_registry = json.loads(target_registry_path.read_text(encoding="utf-8"))
        target_state["registry_version"] = target_registry.get("version", "unknown")
        target_state["variant"] = ""
        pb_state_path = target / "PROGRAMBUILD" / "PROGRAMBUILD_STATE.json"
        if pb_state_path.exists():
            pb_state = json.loads(pb_state_path.read_text(encoding="utf-8"))
            target_state["variant"] = pb_state.get("variant", "")

    # Build comparison
    current_kb = load_knowledge_base()
    kb_version = current_kb.get("version", "unknown")

    deltas: list[str] = []
    if target_state.get("variant") and target_state["variant"] != current_rec.variant:
        deltas.append(f"Variant drift: project uses '{target_state['variant']}', current KB recommends '{current_rec.variant}'")
    if target_state.get("registry_version") and target_state["registry_version"] != load_registry().get("version", ""):
        deltas.append(
            f"Registry version drift: project has '{target_state['registry_version']}', current is '{load_registry().get('version', '')}'"
        )

    return {
        "project_dir": str(target),
        "kickoff_inputs": kickoff_values,
        "product_shape": product_shape,
        "inferred_needs": sorted(needs),
        "current_recommendation": asdict(current_rec),
        "kb_version": kb_version,
        "project_state": target_state,
        "deltas": deltas,
        "re_evaluated_at": datetime.now(UTC).isoformat(timespec="seconds"),
    }


def print_recommendation(recommendation: ProjectRecommendation) -> None:
    print("PROGRAMSTART Recommendation")
    print(f"- product shape: {recommendation.product_shape}")
    print(f"- variant: {recommendation.variant}")
    print(f"- attach USERJOURNEY: {'yes' if recommendation.attach_userjourney else 'no'}")
    print(f"- archetype: {recommendation.archetype}")
    print(f"- confidence: {recommendation.confidence}")
    suggested_stacks = ", ".join(recommendation.stack_names) if recommendation.stack_names else "none matched current KB"
    print(f"- suggested stacks: {suggested_stacks}")
    matched_domains = ", ".join(recommendation.matched_domains) if recommendation.matched_domains else "none matched"
    print(f"- matched domains: {matched_domains}")
    suggested_services = ", ".join(recommendation.service_names) if recommendation.service_names else "none inferred"
    print(f"- suggested services: {suggested_services}")
    suggested_clis = ", ".join(recommendation.cli_tool_names) if recommendation.cli_tool_names else "none inferred"
    print(f"- recommended clis: {suggested_clis}")
    suggested_apis = ", ".join(recommendation.api_names) if recommendation.api_names else "none inferred"
    print(f"- saved api templates: {suggested_apis}")
    print("- rationale:")
    for item in recommendation.rationale:
        print(f"  - {item}")
    if recommendation.coverage_warnings:
        print("- coverage warnings:")
        for item in recommendation.coverage_warnings:
            print(f"  - {item['domain']}: {item['status']} | {item['gaps']}")
    if recommendation.stack_evidence:
        print("- stack evidence:")
        for item in recommendation.stack_evidence[:5]:
            reasons = "; ".join(str(reason) for reason in item.get("reasons", [])[:2])
            print(f"  - {item['name']}: score={item['score']} | {reasons}")
    if recommendation.service_evidence:
        print("- service evidence:")
        for item in recommendation.service_evidence[:5]:
            reasons = "; ".join(str(reason) for reason in item.get("reasons", [])[:2])
            print(f"  - {item['name']}: score={item['score']} | {reasons}")
    if recommendation.api_evidence:
        print("- api evidence:")
        for item in recommendation.api_evidence[:5]:
            reasons = "; ".join(str(reason) for reason in item.get("reasons", [])[:2])
            print(f"  - {item['name']}: score={item['score']} | {reasons}")
    if recommendation.cli_evidence:
        print("- cli evidence:")
        for item in recommendation.cli_evidence[:5]:
            reasons = "; ".join(str(reason) for reason in item.get("reasons", [])[:2])
            print(f"  - {item['name']}: score={item['score']} | {reasons}")
    if recommendation.rule_evidence:
        print("- rule evidence:")
        for item in recommendation.rule_evidence[:5]:
            print(f"  - {item['title']}: {item['because']} ({item['confidence']})")
    if recommendation.actionability_summary:
        print("- actionability summary:")
        for item in recommendation.actionability_summary[:8]:
            print(f"  - {item['name']} [{item['category']}]: {item['actionability']} | {item['reason']}")
    if recommendation.alternatives:
        print("- alternatives:")
        for item in recommendation.alternatives[:4]:
            print(f"  - {item['item']} ({item['category']}): {item['rationale']}")
    if recommendation.service_notes:
        print("- service notes:")
        for item in recommendation.service_notes:
            print(f"  - {item}")
    if recommendation.cli_notes:
        print("- cli notes:")
        for item in recommendation.cli_notes:
            print(f"  - {item}")
    if recommendation.api_notes:
        print("- api notes:")
        for item in recommendation.api_notes:
            print(f"  - {item}")
    print("- kickoff files:")
    for item in recommendation.kickoff_files:
        print(f"  - {item}")
    print("- next commands:")
    for item in recommendation.next_commands:
        print(f"  - {item}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Recommend the right PROGRAMSTART project setup and stack profile.")
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
    parser.add_argument(
        "--re-evaluate",
        metavar="PROJECT_DIR",
        help="Re-evaluate an existing project against the current knowledge base.",
    )
    parser.set_defaults(attach_userjourney=None)
    args = parser.parse_args(argv)

    if args.re_evaluate:
        result = re_evaluate_project(args.re_evaluate)
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print("PROGRAMSTART Re-evaluation Report")
            print(f"- project: {result['project_dir']}")
            print(f"- product shape: {result['product_shape']}")
            print(f"- inferred needs: {', '.join(result['inferred_needs']) or 'none'}")
            print(f"- KB version: {result['kb_version']}")
            print(f"- re-evaluated at: {result['re_evaluated_at']}")
            rec = result["current_recommendation"]
            print(f"- recommended variant: {rec['variant']}")
            print(f"- recommended stacks: {', '.join(rec['stack_names']) or 'none'}")
            print(f"- confidence: {rec['confidence']}")
            if result["deltas"]:
                print("- deltas detected:")
                for d in result["deltas"]:
                    print(f"  - {d}")
            else:
                print("- deltas: none — project aligns with current KB")
        return 0

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
