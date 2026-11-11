# ml-sessions-intent — Task Board

**Updated**: 2026-11-12 by opencode (TOY)

---

## Doing

| ID | Title | Priority | Next |
|----|-------|----------|------|
| **INTENT-02** | ml-repos-analyze 計算コア移植 | P1 | 実データ bronze → notebook |

---

## Planned

| ID | Title | Priority | Next |
|----|-------|----------|------|
| **INTENT-01** | GH metadata baseline（BQML 段なし） | P1 | sample bronze + sklearn |
| **INTENT-03** | Session-wants baseline | P1 | wants.jsonl EDA → TF-IDF |

---

## Done

| ID | Title | Done | Note |
|----|-------|------|------|
| **INTENT-04** | Session→Intent 構造化・自動化 + 登録 | 2026-11-12 | pipeline 実走確認（wiki #374）。wants 12 / intents 4 / sessions 16。canonical は `data/canonical/*.json`+`*.csv`（id 冪等 upsert）、SQLite は処理エンジン |

---

## Pipeline

```
wants/*.yaml   → extract_wants   → bronze/wants.jsonl   ─┐
intents/*.yaml → extract_intents → bronze/intents.jsonl ─┼→ canonical files (JSON/CSV, id upsert)
sessions/      → extract_sessions_index (optional)      ─┘   + SQLite (処理エンジン)
```

```bash
python -m ml_sessions_intent.pipeline
# optional:
python -m ml_sessions_intent.pipeline --sessions-dir /path/to/workspace/sessions
```

Docs: [docs/pipeline.md](./docs/pipeline.md)

---

## 着手順

1. **INTENT-02** — ml-repos-analyze 実データ（今ここ）
2. **INTENT-03** — wants baseline
3. **INTENT-01** — GH metadata baseline
