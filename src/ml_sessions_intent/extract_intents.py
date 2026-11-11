"""Flatten intents/*.yaml into data/bronze/intents.jsonl."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

FIELDS = [
    "id",
    "title",
    "goal",
    "status",
    "priority",
    "source_session",
    "related_kb",
    "related_wants",
    "related_repos",
    "next_action",
    "artifacts",
    "notes",
]


def flatten(intents_dir: Path) -> list[dict]:
    rows: list[dict] = []
    for path in sorted(intents_dir.glob("*.yaml")):
        doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        row = {k: doc.get(k) for k in FIELDS}
        row["_source_file"] = path.name
        rows.append(row)
    return rows


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    intents_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else root / "intents"
    out_path = (
        Path(sys.argv[2])
        if len(sys.argv) > 2
        else root / "data" / "bronze" / "intents.jsonl"
    )
    rows = flatten(intents_dir)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"wrote {len(rows)} rows -> {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
