"""Reject malformed owner evidence before it can become execution authority."""

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from scripts.programstart_authority_resolver import (
    AuthorityResolutionError,
    OwnerAuthorityDeclaration,
    RepositoryAuthorityObservation,
    resolve_repository_authority,
)
from tests.test_programstart_authority_resolver import _declaration, _git, _observation, _repo


@pytest.mark.parametrize("field", ["owning_repository", "observed_head", "methodology_commit"])
@pytest.mark.parametrize("value", [" ", "not-an-object-id"])
def test_observation_requires_owner_and_exact_commits(field: str, value: str, tmp_path: Path) -> None:
    values = dict(
        repository_root=tmp_path, owning_repository="owner/project", observed_head="a" * 40, methodology_commit="b" * 40
    )
    values[field] = value
    if field == "owning_repository" and value != " ":
        assert RepositoryAuthorityObservation.model_validate(values).owning_repository == value
    else:
        with pytest.raises(ValidationError, match="repository observation"):
            RepositoryAuthorityObservation.model_validate(values)


@pytest.mark.parametrize(
    "updates,reason",
    [
        ({"project_name": " "}, "requires project"),
        ({"resource_preflight_path": "plan.json"}, "active owner gate"),
        ({"authority_paths": [" "]}, "must not be empty"),
        ({"authority_paths": ["CURRENT_WORK_PACKET.md"]}, "must be unique"),
        (
            {"parallel_work": [{"name": "lane", "owner": " ", "protected_surfaces": [], "evidence_ref": "other.md"}]},
            "explicit owner",
        ),
        ({"allowed_effects": [" "]}, "empty semantic"),
    ],
)
def test_declaration_rejects_ambiguous_meaning(updates: dict, reason: str) -> None:
    with pytest.raises(ValidationError, match=reason):
        OwnerAuthorityDeclaration.model_validate(_declaration(**updates))


@pytest.mark.parametrize(
    "change,reason",
    [
        ("invalid-json", "declaration is invalid"),
        ("foreign", "repository does not match"),
        ("self-reference", "own artifact reference"),
        ("backslash", "unsafe"),
        ("control", "unsafe"),
        ("oversized-plan", "exceeds bounded size"),
    ],
)
def test_committed_invalid_owner_evidence_fails_closed(tmp_path: Path, change: str, reason: str) -> None:
    declaration = _declaration()
    if change == "foreign":
        declaration["owning_repository"] = "foreign/project"
    elif change == "self-reference":
        declaration["authority_paths"] = [".programstart/authority.json"]
    elif change in {"backslash", "control"}:
        declaration["authority_paths"] = ["docs\\master.md" if change == "backslash" else "docs/ma\nster.md"]
    elif change == "oversized-plan":
        declaration.update(resource_preflight_required=True, resource_preflight_path=".programstart/plan.json")
    root, _ = _repo(tmp_path, declaration)
    if change == "invalid-json":
        (root / ".programstart/authority.json").write_text("{")
    elif change == "oversized-plan":
        (root / ".programstart/plan.json").write_text(json.dumps({"payload": "x" * 16384}))
    _git(root, "add", ".")
    _git(root, "commit", "--allow-empty", "-m", "invalid evidence fixture")
    head = _git(root, "rev-parse", "HEAD")
    with pytest.raises(AuthorityResolutionError, match=reason):
        resolve_repository_authority(_observation(root, head))
    assert _git(root, "rev-parse", "HEAD") == head
    assert _git(root, "status", "--porcelain") == ""


def test_missing_root_and_non_git_root_cannot_resolve(tmp_path: Path) -> None:
    for root, reason in [(tmp_path / "absent", "does not exist"), (tmp_path, "Git repository")]:
        with pytest.raises(AuthorityResolutionError, match=reason):
            resolve_repository_authority(_observation(root, "a" * 40))
