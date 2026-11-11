from ml_sessions_intent.intent import list_intents, load_intent
from ml_sessions_intent.schema import load_schema
from pathlib import Path


def test_schema_loads():
    s = load_schema()
    assert "intent" in s


def test_sample_intent_exists():
    intents = list_intents()
    assert len(intents) >= 1
    assert any(i.get("id") == "INTENT-2026-11-11-01" for i in intents)
