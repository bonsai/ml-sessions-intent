import json

from ml_sessions_intent.extract_intents import flatten as flatten_intents
from ml_sessions_intent.extract_wants import flatten as flatten_wants
from ml_sessions_intent.db import connect, emit_files, upsert_intents, upsert_wants
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


def test_emit_files(tmp_path):
    bronze = tmp_path / "bronze"
    bronze.mkdir()
    (bronze / "intents.jsonl").write_text(
        '{"id": "I1", "title": "t", "_source_file": "x.yaml"}\n', encoding="utf-8"
    )
    canonical = tmp_path / "canonical"
    res = emit_files(bronze, canonical)
    assert res == {"sessions": 0, "wants": 0, "intents": 1}
    rows = json.loads((canonical / "intents.json").read_text(encoding="utf-8"))
    assert rows[0]["id"] == "I1"
    assert rows[0]["source_file"] == "x.yaml"  # row _source_file maps to column
    assert rows[0]["next_action"] is None  # missing columns filled
    assert (canonical / "intents.csv").exists()


def test_emit_files_idempotent_and_preserves_extra(tmp_path):
    bronze = tmp_path / "bronze"
    bronze.mkdir()
    (bronze / "wants.jsonl").write_text(
        '{"id": "W1", "title": "a", "related": ["x"]}\n', encoding="utf-8"
    )
    canonical = tmp_path / "canonical"
    emit_files(bronze, canonical)
    # a row added elsewhere (e.g. a future proposal) must survive a re-run
    (canonical / "wants.json").write_text(
        json.dumps(
            [
                {"id": "W1", "title": "stale"},
                {"id": "W-proposal", "title": "keep me"},
            ],
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    emit_files(bronze, canonical)
    rows = json.loads((canonical / "wants.json").read_text(encoding="utf-8"))
    by_id = {r["id"]: r for r in rows}
    assert by_id["W1"]["title"] == "a"  # bronze wins
    assert by_id["W-proposal"]["title"] == "keep me"  # existing-only preserved
