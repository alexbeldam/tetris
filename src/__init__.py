"""
Bloquinhos - A Tetris-inspired game implementation.

This package contains the core game logic, UI, networking,
and utility modules for the Bloquinhos game.
"""

from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
import re


def _read_project_version() -> str:
	try:
		return version("bloquinhos")
	except PackageNotFoundError:
		project_root = Path(__file__).resolve().parent.parent
		pyproject_path = project_root / "pyproject.toml"
		if pyproject_path.exists():
			content = pyproject_path.read_text(encoding="utf-8")
			match = re.search(r'^version\s*=\s*"([^"]+)"', content, re.MULTILINE)
			if match:
				return match.group(1)
		return "0.0.0"


__version__ = _read_project_version()