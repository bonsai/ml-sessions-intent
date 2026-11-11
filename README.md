# ml-sessions-intent

Session → Want → Intent の薄いハブ（正は YAML + JSON/CSV、SQLite は処理エンジン）。

**Pipeline**: [docs/pipeline.md](./docs/pipeline.md)  
**Tasks**: [TASKS.md](./TASKS.md)

---

## Quick run

```bash
pip install -e ".[dev]"
python -m ml_sessions_intent.pipeline
# → data/bronze/*.jsonl + data/canonical/*.json + *.csv (+ ml_sessions.db)
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
| Canonical | `data/canonical/*.json` + `*.csv` | 正の集約（id で冪等 upsert、gitignore） |
| Engine DB | `data/canonical/ml_sessions.db` | SQLite（処理エンジン、再生成可、gitignore） |

---

## Current intents

| ID | Title | Status |
|----|-------|--------|
| INTENT-04 | Session→Intent 自動化 + 登録 | **done** |
| INTENT-02 | ml-repos-analyze 移植 | doing |
| INTENT-01 | GH metadata baseline | planned |
| INTENT-03 | Session-wants baseline | planned |
