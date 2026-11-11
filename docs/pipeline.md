# Session → Intent パイプライン

**Goal**: セッションからやりたいことを拾い、intent に整理し、DB に登録する流れを構造化・自動化する。

```
sessions/ (workspace)
    │  extract_sessions_index.py   → data/bronze/sessions.jsonl
    ▼
wants/*.yaml  (人手 or エージェント抽出)
    │  extract_wants.py            → data/bronze/wants.jsonl
    ▼
intents/*.yaml  (実験単位に落とす)
    │  extract_intents.py          → data/bronze/intents.jsonl
    ▼
SQLite  data/canonical/ml_sessions.db
    │  db.register_all()
    ▼
TASKS.md / notebook / Kaggle
```

## 原則

1. **Canonical** = YAML（wants / intents）+ SQLite
2. **Bronze** = JSONL（派生・EDA用）
3. セッション本文は最初は読まない（index + 構造化フィールドのみ）
4. DB は冪等 upsert（id がキー）

## コマンド

```bash
# 一式
python -m ml_sessions_intent.pipeline

# 個別
python -m ml_sessions_intent.extract_wants
python -m ml_sessions_intent.extract_intents
python -m ml_sessions_intent.db --init --load
```
