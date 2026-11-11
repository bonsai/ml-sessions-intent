"""Canonical store for sessions / wants / intents.

Canonical (the source of truth) is the file aggregation in
data/canonical/ — ``<table>.json`` + ``<table>.csv``, upserted by id.
SQLite (data/canonical/ml_sessions.db) is kept as a *processing engine*
only: it is convenient for ad-hoc SQL and can be regenerated at any time.
Bronze JSONL stays the load source for both.

See docs/pipeline.md ("原則").
"""

from __future__ import annotations

import csv
import json
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CANONICAL = ROOT / "data" / "canonical"
DEFAULT_DB = CANONICAL / "ml_sessions.db"
BRONZE = ROOT / "data" / "bronze"

# Primary key and column order per canonical table. The key is the id used
# for idempotent upsert into the JSON/CSV files.
CANONICAL_KEYS = {"sessions": "session_file_id", "wants": "id", "intents": "id"}
CANONICAL_COLUMNS = {
    "sessions": ["session_file_id", "agent", "date", "filename", "kind", "source_path"],
    "wants": [
        "id", "session", "extracted_by", "title", "intensity", "status",
        "cluster", "related", "depends_on", "enables", "learning", "source",
    ],
    "intents": [
        "id", "title", "goal", "status", "priority", "source_session",
        "related_kb", "related_wants", "related_repos", "next_action",
        "artifacts", "notes", "source_file",
    ],
}

SCHEMA = """
CREATE TABLE IF NOT EXISTS sessions (
  session_file_id TEXT PRIMARY KEY,
  agent TEXT,
  date TEXT,
  filename TEXT,
  kind TEXT,
  source_path TEXT
);

CREATE TABLE IF NOT EXISTS wants (
  id TEXT PRIMARY KEY,
  session TEXT,
  extracted_by TEXT,
  title TEXT,
  intensity REAL,
  status TEXT,
  cluster TEXT,
  related TEXT,      -- JSON array
  depends_on TEXT,   -- JSON array
  enables TEXT,      -- JSON array
  learning TEXT,
  source TEXT
);

CREATE TABLE IF NOT EXISTS intents (
  id TEXT PRIMARY KEY,
  title TEXT,
  goal TEXT,
  status TEXT,
  priority TEXT,
  source_session TEXT,
  related_kb TEXT,       -- JSON
  related_wants TEXT,    -- JSON
  related_repos TEXT,    -- JSON
  next_action TEXT,
  artifacts TEXT,        -- JSON
  notes TEXT,
  source_file TEXT
);
"""


def connect(db_path: Path | None = None) -> sqlite3.Connection:
    path = db_path or DEFAULT_DB
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.executescript(SCHEMA)
    return conn


def _j(v):
    if v is None:
        return None
    if isinstance(v, (list, dict)):
        return json.dumps(v, ensure_ascii=False)
    return v


def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def upsert_sessions(conn: sqlite3.Connection, rows: list[dict]) -> int:
    sql = """
    INSERT INTO sessions (session_file_id, agent, date, filename, kind, source_path)
    VALUES (:session_file_id, :agent, :date, :filename, :kind, :source_path)
    ON CONFLICT(session_file_id) DO UPDATE SET
      agent=excluded.agent, date=excluded.date, filename=excluded.filename,
      kind=excluded.kind, source_path=excluded.source_path
    """
    conn.executemany(sql, rows)
    return len(rows)


def upsert_wants(conn: sqlite3.Connection, rows: list[dict]) -> int:
    prepared = []
    for r in rows:
        prepared.append({
            "id": r.get("id"),
            "session": r.get("session"),
            "extracted_by": r.get("extracted_by"),
            "title": r.get("title"),
            "intensity": r.get("intensity"),
            "status": r.get("status"),
            "cluster": r.get("cluster"),
            "related": _j(r.get("related")),
            "depends_on": _j(r.get("depends_on")),
            "enables": _j(r.get("enables")),
            "learning": r.get("learning"),
            "source": r.get("source"),
        })
    sql = """
    INSERT INTO wants (id, session, extracted_by, title, intensity, status, cluster,
                       related, depends_on, enables, learning, source)
    VALUES (:id, :session, :extracted_by, :title, :intensity, :status, :cluster,
            :related, :depends_on, :enables, :learning, :source)
    ON CONFLICT(id) DO UPDATE SET
      session=excluded.session, extracted_by=excluded.extracted_by,
      title=excluded.title, intensity=excluded.intensity, status=excluded.status,
      cluster=excluded.cluster, related=excluded.related,
      depends_on=excluded.depends_on, enables=excluded.enables,
      learning=excluded.learning, source=excluded.source
    """
    conn.executemany(sql, prepared)
    return len(prepared)


def upsert_intents(conn: sqlite3.Connection, rows: list[dict]) -> int:
    prepared = []
    for r in rows:
        prepared.append({
            "id": r.get("id"),
            "title": r.get("title"),
            "goal": r.get("goal"),
            "status": r.get("status"),
            "priority": r.get("priority"),
            "source_session": r.get("source_session"),
            "related_kb": _j(r.get("related_kb")),
            "related_wants": _j(r.get("related_wants")),
            "related_repos": _j(r.get("related_repos")),
            "next_action": r.get("next_action"),
            "artifacts": _j(r.get("artifacts")),
            "notes": r.get("notes"),
            "source_file": r.get("_source_file"),
        })
    sql = """
    INSERT INTO intents (id, title, goal, status, priority, source_session,
                         related_kb, related_wants, related_repos,
                         next_action, artifacts, notes, source_file)
    VALUES (:id, :title, :goal, :status, :priority, :source_session,
            :related_kb, :related_wants, :related_repos,
            :next_action, :artifacts, :notes, :source_file)
    ON CONFLICT(id) DO UPDATE SET
      title=excluded.title, goal=excluded.goal, status=excluded.status,
      priority=excluded.priority, source_session=excluded.source_session,
      related_kb=excluded.related_kb, related_wants=excluded.related_wants,
      related_repos=excluded.related_repos, next_action=excluded.next_action,
      artifacts=excluded.artifacts, notes=excluded.notes,
      source_file=excluded.source_file
    """
    conn.executemany(sql, prepared)
    return len(prepared)


def register_all(db_path: Path | None = None) -> dict:
    conn = connect(db_path)
    n_s = upsert_sessions(conn, load_jsonl(BRONZE / "sessions.jsonl"))
    n_w = upsert_wants(conn, load_jsonl(BRONZE / "wants.jsonl"))
    n_i = upsert_intents(conn, load_jsonl(BRONZE / "intents.jsonl"))
    conn.commit()
    conn.close()
    return {"sessions": n_s, "wants": n_w, "intents": n_i,
            "db": str(db_path or DEFAULT_DB)}


def _normalize(table: str, row: dict) -> dict:
    """Keep only the canonical columns and fill the rest with None.

    intents bronze rows carry the source file as ``_source_file``; the
    canonical file names that column ``source_file``.
    """
    if table == "intents":
        row = {**row, "source_file": row.get("source_file") or row.get("_source_file")}
    return {col: row.get(col) for col in CANONICAL_COLUMNS[table]}


def _merge_by_key(existing: list[dict], incoming: list[dict], key: str) -> list[dict]:
    """Idempotent upsert: incoming wins, existing-only rows are preserved."""
    merged: dict = {}
    for row in existing:
        merged[str(row.get(key))] = row
    for row in incoming:
        merged[str(row.get(key))] = row
    return [merged[k] for k in sorted(merged)]


def _load_json_list(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, rows: list[dict]) -> None:
    path.write_text(
        json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def _csv_value(v):
    if isinstance(v, (list, dict)):
        return json.dumps(v, ensure_ascii=False)
    return v


def _write_csv(path: Path, rows: list[dict], columns: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({c: _csv_value(row.get(c)) for c in columns})


def emit_files(bronze_dir: Path | None = None, canonical_dir: Path | None = None) -> dict:
    """Write the canonical JSON/CSV aggregation from bronze JSONL.

    Each table is merged with the existing canonical file by its primary
    key, so re-running is idempotent and rows added elsewhere (e.g. a
    future proposal) survive. No session transcript text is read.
    """
    bronze = bronze_dir or BRONZE
    out_dir = canonical_dir or CANONICAL
    out_dir.mkdir(parents=True, exist_ok=True)
    result = {}
    for table, key in CANONICAL_KEYS.items():
        columns = CANONICAL_COLUMNS[table]
        incoming = [_normalize(table, r) for r in load_jsonl(bronze / f"{table}.jsonl")]
        existing = _load_json_list(out_dir / f"{table}.json")
        merged = _merge_by_key(existing, incoming, key)
        _write_json(out_dir / f"{table}.json", merged)
        _write_csv(out_dir / f"{table}.csv", merged, columns)
        result[table] = len(merged)
    return result


def main() -> int:
    args = sys.argv[1:]
    do_init = "--init" in args or "--load" in args or not args
    do_load = "--load" in args or not args
    if do_init:
        connect()  # ensures schema
        print(f"schema ok -> {DEFAULT_DB}")
    if do_load:
        stats = register_all()
        print(f"registered: {stats}")
        print(f"canonical files: {emit_files()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
