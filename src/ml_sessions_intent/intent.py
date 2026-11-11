"""Load and list intent YAML files."""

from pathlib import Path
from typing import Any

import yaml

INTENTS_DIR = Path(__file__).resolve().parents[2] / "intents"


def load_intent(path: str | Path) -> dict[str, Any]:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def list_intents(directory: Path | None = None) -> list[dict[str, Any]]:
    d = directory or INTENTS_DIR
    intents = []
    for p in sorted(d.glob("*.yaml")):
        intents.append(load_intent(p))
    return intents


def intents_by_status(status: str, directory: Path | None = None) -> list[dict[str, Any]]:
    return [i for i in list_intents(directory) if i.get("status") == status]
