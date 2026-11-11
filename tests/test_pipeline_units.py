from ml_sessions_intent.extract_intents import flatten as flatten_intents
from ml_sessions_intent.extract_wants import flatten as flatten_wants
from ml_sessions_intent.db import connect, upsert_intents, upsert_wants
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_flatten_intents():
    rows = flatten_intents(ROOT / "intents")
    assert len(rows) >= 2
    ids = {r["id"] for r in rows}
    assert "INTENT-2026-11-11-01" in ids


def test_flatten_wants():
    rows = flatten_wants(ROOT / "wants")
    assert len(rows) >= 1


def test_db_upsert(tmp_path):
    db = tmp_path / "t.db"
    conn = connect(db)
    n = upsert_intents(conn, [{
        "id": "INTENT-TEST",
        "title": "t",
        "goal": "g",
        "status": "planned",
        "priority": "P2",
        "_source_file": "x.yaml",
    }])
    conn.commit()
    assert n == 1
    cur = conn.execute("select id from intents")
    assert cur.fetchone()[0] == "INTENT-TEST"
    conn.close()
