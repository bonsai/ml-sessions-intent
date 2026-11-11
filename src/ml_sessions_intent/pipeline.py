"""Run full bronze extract + SQLite registration.

Does not clone workspace; expects wants/ and intents/ in this repo.
Sessions index is optional (pass --sessions-dir).
"""

from __future__ import annotations

import sys
from pathlib import Path

from ml_sessions_intent.extract_intents import flatten as flatten_intents
from ml_sessions_intent.extract_wants import flatten as flatten_wants
from ml_sessions_intent.db import register_all, DEFAULT_DB
import json


def write_jsonl(rows: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    bronze = root / "data" / "bronze"

    wants = flatten_wants(root / "wants")
    write_jsonl(wants, bronze / "wants.jsonl")
    print(f"wants: {len(wants)} -> bronze/wants.jsonl")

    intents = flatten_intents(root / "intents")
    write_jsonl(intents, bronze / "intents.jsonl")
    print(f"intents: {len(intents)} -> bronze/intents.jsonl")

    # sessions index only if dir provided
    if "--sessions-dir" in sys.argv:
        idx = sys.argv.index("--sessions-dir")
        sessions_dir = Path(sys.argv[idx + 1])
        from ml_sessions_intent.extract_sessions_index import index
        sessions = index(sessions_dir)
        write_jsonl(sessions, bronze / "sessions.jsonl")
        print(f"sessions: {len(sessions)} -> bronze/sessions.jsonl")

    stats = register_all()
    print(f"db: {stats}")
    print(f"canonical db path: {DEFAULT_DB}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
