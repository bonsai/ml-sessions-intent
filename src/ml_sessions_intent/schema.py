"""Load intent schema."""

from pathlib import Path
from typing import Any

import yaml

SCHEMA_PATH = Path(__file__).resolve().parents[2] / "schema" / "intent.yaml"


def load_schema(path: Path | None = None) -> dict[str, Any]:
    p = path or SCHEMA_PATH
    with open(p, encoding="utf-8") as f:
        return yaml.safe_load(f)
