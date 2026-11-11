"""Flatten wants/*.yaml into data/bronze/wants.jsonl.

One row per want, following schema/want.yaml. Index/metadata only —
no session transcript text is read.

Usage:
    python -m ml_sessions_intent.extract_wants [wants_dir] [out_path]
Defaults: wants/ -> data/bronze/wants.jsonl (repo root relative).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

FIELDS = [
    "id", "session", "extracted_by", "title", "intensity", "status",
    "cluster", "related", "depends_on", "enables", "learning", "source",
]


def flatten(wants_dir: Path) -> list[dict]:
    rows: list[dict] = []
    for path in sorted(wants_dir.glob("*.yaml")):
        doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        session = doc.get("session")
        extracted_by = doc.get("extracted_by")
        for want in doc.get("wants", []):
            row = {k: want.get(k) for k in FIELDS}
            row["session"] = want.get("session") or session
            row["extracted_by"] = extracted_by
            rows.append(row)
    return rows


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    wants_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else root / "wants"
    out_path = Path(sys.argv[2]) if len(sys.argv) > 2 else root / "data" / "bronze" / "wants.jsonl"
    rows = flatten(wants_dir)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"wrote {len(rows)} rows -> {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
