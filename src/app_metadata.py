"""Application metadata helpers."""

import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PYPROJECT_PATH = PROJECT_ROOT / "pyproject.toml"
DEFAULT_VERSION = "0.0.0"


def get_project_version(pyproject_path: Path = PYPROJECT_PATH) -> str:
    """Read the application version from pyproject.toml."""
    if not pyproject_path.exists():
        return DEFAULT_VERSION

    content = pyproject_path.read_text(encoding="utf-8")
    match = re.search(r'^version\s*=\s*"([^"]+)"', content, re.MULTILINE)
    if match is None:
        return DEFAULT_VERSION

    return match.group(1)
