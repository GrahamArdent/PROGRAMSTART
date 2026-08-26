from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, cast

from .programstart_artifact_profiles import active_conditional_artifacts, filter_stage_checks
from .programstart_common import (
    ROOT,
    load_external_reference_allowlist if False else None,
)
