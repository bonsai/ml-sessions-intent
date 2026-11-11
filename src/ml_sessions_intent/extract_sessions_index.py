"""Index the session files under bonsai/workspace/sessions/ into
data/bronze/sessions.jsonl.

Index-only: file names and locations are the data — file contents are
never read. Layout assumption: sessions/<agent>/*.md with the agent
folders (muse / grok / chatgpt / ...); files directly under sessions/
are tagged agent="shared".

Usage:
    python -m ml_sessions_intent.extract_sessions_index <sessions_dir> [out_path]
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

DATE_RE = re.compile(r"^(20\d{2}-\d{2}-\d{2})")


def kind_of(name: str) -> str:
    low = name.lower()
    if low in ("index.md", "readme.md"):
        return "index"
    if "topics" in low:
        return "topics"
    if "wants" in low:
        return "wants"
    if "session" in low or "summary" in low:
        return "summary"
    if low.endswith((".json", ".html")):
        return "data"
    return "other"


def index(sessions_dir: Path) -> list[dict]:
    rows: list[dict] = []
    files: list[tuple[str, Path]] = []
    for p in sorted(sessions_dir.iterdir()):
        if p.is_file():
            files.append(("shared", p))
        elif p.is_dir():
            for q in sorted(p.iterdir()):
                if q.is_file():
                    files.append((p.name, q))
    for agent, path in files:
        m = DATE_RE.match(path.name)
        rows.append({
            "session_file_id": f"{agent}/{path.name}",
            "agent": agent,
            "date": m.group(1) if m else None,
            "filename": path.name,
            "kind": kind_of(path.name),
            "source_path": f"sessions/{agent}/{path.name}" if agent != "shared"
                           else f"sessions/{path.name}",
        })
    return rows


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: extract_sessions_index <sessions_dir> [out_path]")
        return 2
    sessions_dir = Path(sys.argv[1])
    root = Path(__file__).resolve().parents[2]
    out_path = Path(sys.argv[2]) if len(sys.argv) > 2 else root / "data" / "bronze" / "sessions.jsonl"
    rows = index(sessions_dir)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"wrote {len(rows)} rows -> {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
