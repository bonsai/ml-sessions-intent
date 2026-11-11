# ml-sessions-intent

ML session intents & structured wants.

**Author note**: Scaffold + extractions by Grok / Muse — 2026-11-11

---

## Task board

→ **[TASKS.md](./TASKS.md)**（Doing / Planned / 依存 / 着手順）

---

## Two layers

| Layer | Path | Role |
|-------|------|------|
| **Want** | `wants/` | Session-extracted やりたいこと（濃さ / 関連 / 依存 / 学習） |
| **Intent** | `intents/` | Experiment-sized unit（goal → next_action → artifacts） |
| **Bronze** | `data/bronze/` | JSONL derived from YAML（EDA / baseline 用） |

Want が先 → Intent に落とす、という流れ。

---

## Current intents

| ID | Title | Status |
|----|-------|--------|
| INTENT-01 | BQML-style GH metadata baseline on Kaggle | planned |
| INTENT-02 | ml-repos-analyze 計算コア移植 | **doing** |
| INTENT-03 | Session-wants baseline（title→cluster） | planned |

---

## Layout

```
intents/
wants/
data/bronze/
schema/
src/ml_sessions_intent/
notebooks/
TASKS.md
```
