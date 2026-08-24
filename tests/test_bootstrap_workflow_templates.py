from __future__ import annotations

from pathlib import Path

from scripts import programstart_attach as attach
from scripts import programstart_bootstrap as bootstrap
from scripts import programstart_sync as sync


def _registry(*assets: str) -> dict:
    return {
        "workspace": {"bootstrap_assets": list(assets)},
        "prompt_registry": {},
        "workflow_guidance": {},
    }


def test_materialized_bootstrap_asset_path_maps_workflow_templates() -> None:
    assert (
        bootstrap.materialized_bootstrap_asset_path("templates/github-workflows/process-guardrails.yml")
        == ".github/workflows/process-guardrails.yml"
    )


def test_materialized_bootstrap_asset_path_leaves_normal_assets_unchanged() -> None:
    assert bootstrap.materialized_bootstrap_asset_path("docs/toolchain.md") == "docs/toolchain.md"


def test_generated_repo_bootstrap_assets_expose_canonical_workflow_paths() -> None:
    registry = _registry(
        "templates/github-workflows/docs-pages.yml",
        "templates/github-workflows/codeql.yml",
        "README.md",
    )

    assets = bootstrap.generated_repo_bootstrap_assets(registry)

    assert ".github/workflows/docs-pages.yml" in assets
    assert ".github/workflows/codeql.yml" in assets
    assert "templates/github-workflows/docs-pages.yml" not in assets
    assert "README.md" in assets


def test_bootstrap_shared_assets_materializes_workflow_template(monkeypatch, tmp_path: Path) -> None:
    template_root = tmp_path / "template"
    source = template_root / "templates" / "github-workflows" / "process-guardrails.yml"
    source.parent.mkdir(parents=True)
    source.write_text("name: CI Guardrails\n", encoding="utf-8")

    destination_root = tmp_path / "project"
    registry = _registry("templates/github-workflows/process-guardrails.yml")
    monkeypatch.setattr(bootstrap, "workspace_path", lambda relative: template_root / relative)

    bootstrap.bootstrap_shared_assets(destination_root, registry, dry_run=False)

    materialized = destination_root / ".github" / "workflows" / "process-guardrails.yml"
    assert materialized.read_text(encoding="utf-8") == "name: CI Guardrails\n"
    assert not (destination_root / "templates" / "github-workflows" / "process-guardrails.yml").exists()


def test_attach_programbuild_assets_materializes_workflow_template(monkeypatch, tmp_path: Path) -> None:
    template_root = tmp_path / "template"
    source = template_root / "templates" / "github-workflows" / "docs-pages.yml"
    source.parent.mkdir(parents=True)
    source.write_text("name: Docs Build And Deploy\n", encoding="utf-8")

    destination_root = tmp_path / "existing-project"
    destination_root.mkdir()
    registry = _registry("templates/github-workflows/docs-pages.yml")
    monkeypatch.setattr(attach, "workspace_path", lambda _relative: template_root)

    copied = attach._copy_programbuild_bootstrap_assets(destination_root, registry)

    materialized = destination_root / ".github" / "workflows" / "docs-pages.yml"
    assert materialized.read_text(encoding="utf-8") == "name: Docs Build And Deploy\n"
    assert copied == [".github/workflows/docs-pages.yml"]


def test_sync_resolves_materialized_workflow_to_dormant_template(tmp_path: Path) -> None:
    template_root = tmp_path / "template"
    dormant = template_root / "templates" / "github-workflows" / "codeql.yml"
    dormant.parent.mkdir(parents=True)
    dormant.write_text("name: CodeQL\n", encoding="utf-8")

    resolved = sync._template_source_path(template_root, ".github/workflows/codeql.yml")

    assert resolved == dormant


def test_sync_prefers_direct_workflow_source_when_present(tmp_path: Path) -> None:
    template_root = tmp_path / "template"
    direct = template_root / ".github" / "workflows" / "codeql.yml"
    direct.parent.mkdir(parents=True)
    direct.write_text("name: Active CodeQL\n", encoding="utf-8")
    dormant = template_root / "templates" / "github-workflows" / "codeql.yml"
    dormant.parent.mkdir(parents=True)
    dormant.write_text("name: Dormant CodeQL\n", encoding="utf-8")

    resolved = sync._template_source_path(template_root, ".github/workflows/codeql.yml")

    assert resolved == direct
