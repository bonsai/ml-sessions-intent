# ml-sessions-intent — Task Board

**Updated**: 2026-11-11 by Grok

---

## Doing

| ID | Title | Priority | Next |
|----|-------|----------|------|
| **INTENT-04** | Session→Intent 構造化・自動化 + DB登録 | **P0** | `python -m ml_sessions_intent.pipeline` 実行・確認 |
| **INTENT-02** | ml-repos-analyze 計算コア移植 | P1 | 実データ bronze → notebook |

---

## Planned

| ID | Title | Priority | Next |
|----|-------|----------|------|
| **INTENT-01** | BQML-style GH metadata baseline | P1 | sample bronze + sklearn |
| **INTENT-03** | Session-wants baseline | P1 | wants.jsonl EDA → TF-IDF |

---

## Pipeline（新規）

```
wants/*.yaml  → extract_wants   → bronze/wants.jsonl  ─┐
intents/*.yaml → extract_intents → bronze/intents.jsonl ─┼→ SQLite upsert
sessions/      → extract_sessions_index (optional)      ─┘
```

```bash
python -m ml_sessions_intent.pipeline
# optional:
python -m ml_sessions_intent.pipeline --sessions-dir /path/to/workspace/sessions
```

Docs: [docs/pipeline.md](./docs/pipeline.md)

---

## 着手順

1. **INTENT-04** — パイプラインを一度通す（今ここ）
2. **INTENT-02** — ml-repos-analyze 実データ
3. **INTENT-03** — wants baseline
4. **INTENT-01** — GH metadata baseline
