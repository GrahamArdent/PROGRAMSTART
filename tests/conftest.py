from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"

if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))


def userjourney_attached() -> bool:
    """Return True when a USERJOURNEY directory exists in this repo."""
    return (ROOT / "USERJOURNEY").is_dir()


requires_userjourney = pytest.mark.skipif(
    not userjourney_attached(),
    reason="USERJOURNEY not attached to this repository",
)


@pytest.fixture()
def workspace_root() -> Path:
    """Return the resolved workspace root path."""
    return ROOT


@pytest.fixture()
def config_dir() -> Path:
    """Return the config directory path."""
    return ROOT / "config"


@pytest.fixture()
def scripts_dir() -> Path:
    """Return the scripts directory path."""
    return SCRIPTS
