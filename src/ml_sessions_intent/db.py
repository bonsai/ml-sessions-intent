"""SQLite canonical store for sessions / wants / intents.

Canonical path: data/canonical/ml_sessions.db
Upsert by primary id. Bronze JSONL is the load source.
"""

from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DB = ROOT / "data" / "canonical" / "ml_sessions.db"
BRONZE = ROOT / "data" / "bronze"

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
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
