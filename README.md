# ml-sessions-intent

Session → Want → Intent → SQLite の薄いハブ。

**Pipeline**: [docs/pipeline.md](./docs/pipeline.md)  
**Tasks**: [TASKS.md](./TASKS.md)

---

## Quick run

```bash
pip install -e ".[dev]"
python -m ml_sessions_intent.pipeline
# → data/bronze/*.jsonl + data/canonical/ml_sessions.db
```

```bash
python -m ml_sessions_intent.pipeline --sessions-dir ../workspace/sessions
```

---

## Layers

| Layer | Path | Role |
|-------|------|------|
| Want YAML | `wants/` | セッションから拾ったやりたいこと |
| Intent YAML | `intents/` | 実験単位 |
| Bronze | `data/bronze/` | JSONL（EDA） |
| Canonical DB | `data/canonical/ml_sessions.db` | SQLite（gitignore） |

---

## Current intents

| ID | Title | Status |
|----|-------|--------|
| INTENT-04 | Session→Intent 自動化 + DB | **doing** |
| INTENT-02 | ml-repos-analyze 移植 | doing |
| INTENT-01 | BQML GH metadata baseline | planned |
| INTENT-03 | Session-wants baseline | planned |
