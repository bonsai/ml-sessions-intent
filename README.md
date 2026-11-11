# ml-sessions-intent

ML session intents & experiment tracking template.

Derived from [kaggle-bqml-core](https://github.com/bonsai/kaggle-bqml-core).

**Purpose**: session logs → structured ML intents → runnable experiments / artifacts.

**Author note**: Scaffold by Grok (xAI) — 2026-11-11

---

## Idea

1. Sessions produce *intents* (what we want to learn / build)
2. Intents are captured as YAML (machine-readable)
3. Each intent can spawn a small experiment (notebook / script)
4. Results and decisions feed back into the next session

This repo is the shared skeleton for that loop.

---

## Layout

```
.
├── README.md
├── pyproject.toml
├── schema/
│   └── intent.yaml          # intent schema
├── intents/                 # one YAML per intent
│   └── .gitkeep
├── sessions/                # optional session summaries (links)
│   └── .gitkeep
├── notebooks/
│   └── 01_intent_to_baseline.ipynb
├── src/ml_sessions_intent/
│   ├── schema.py
│   ├── intent.py            # load / validate intents
│   └── io.py
├── tests/
└── .github/workflows/ci.yml
```

---

## Quick start

1. Copy an intent template into `intents/`
2. Fill `goal`, `source_session`, `status`, `next_action`
3. Point a notebook at it and run a minimal baseline
4. Update the intent YAML with results / decisions

---

## Relation to other repos

| Repo | Role |
|------|------|
| `bonsai/workspace` | Session logs & kanban (source of intents) |
| `bonsai/kaggle-bqml-core` | Shared data/feature foundation for BQML-style work |
| `bonsai/ml-sessions-intent` | **This repo** — intent capture + experiment loop |
