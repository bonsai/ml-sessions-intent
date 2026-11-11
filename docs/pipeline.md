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
canonical files  data/canonical/{sessions,wants,intents}.json + .csv
    │  db.emit_files()        （id で冪等 upsert）
    │  db.register_all()      （SQLite = 処理エンジン、再生成可能）
    ▼
TASKS.md / notebook / Kaggle
```

## 原則

1. **Canonical** = YAML（wants / intents）+ ファイル集約（`data/canonical/<table>.json` / `.csv`、id で冪等 upsert）
2. **Bronze** = JSONL（派生・EDA用）
3. セッション本文は最初は読まない（index + 構造化フィールドのみ）
4. SQLite（`data/canonical/ml_sessions.db`）は**処理エンジン**（ad-hoc SQL 用）。正の置き場ではなく、いつでも再生成できる
5. ファイル集約も冪等 upsert（id がキー）。bronze に無い既存行は保持する

> 方針変更（2026-11-11 夜）: 従来の「Canonical = YAML + SQLite」は supersede。
> 正は JSON/CSV/YAML、SQLite は処理エンジン。

## コマンド

```bash
# 一式
python -m ml_sessions_intent.pipeline

# 個別
python -m ml_sessions_intent.extract_wants
python -m ml_sessions_intent.extract_intents
python -m ml_sessions_intent.db --init --load
```
