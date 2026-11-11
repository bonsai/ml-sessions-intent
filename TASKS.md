# ml-sessions-intent — Task Board

**Updated**: 2026-11-11 by Grok

Intent を「今やること」単位に並べたボード。  
詳細は各 `intents/*.yaml` を正とする。

---

## Doing（進行中）

| ID | Title | Priority | Next action（要約） |
|----|-------|----------|---------------------|
| **INTENT-02** | ml-repos-analyze への計算コア移植 | P1 | 実データ bronze → notebook 実行 → overall/status/layer 確認 |

---

## Planned（次にやる）

| ID | Title | Priority | Next action（要約） |
|----|-------|----------|---------------------|
| **INTENT-01** | BQML-style GH metadata baseline on Kaggle | P1 | kaggle-bqml-core に sample bronze を置き、EDA + sklearn baseline |
| **INTENT-03** | Session-wants baseline（title→cluster） | P1 | wants.jsonl で EDA → TF-IDF + logistic の baseline |

---

## 依存関係

```
INTENT-02 (ml-repos-analyze 移植)     ← 実repo health データが取れる
        │
        └─ 参考になる → INTENT-01 (GH metadata / time-to-close)
                         ※ 両方とも Kaggle + bronze パターン

INTENT-03 (wants baseline)            ← このrepo内の wants.jsonl で完結
        │
        └─ W-06「濃さ・関連・依存の構造化」の学習ループ入口
```

---

## 推奨する着手順

1. **INTENT-02** を仕上げる（repo は既にある → 実データ1本通すだけ）
2. **INTENT-03** で wants の EDA（データは既に bronze にある）
3. **INTENT-01** は sample を用意してから（KB-009 本番に近い）

---

## Done / 基盤（このrepoで既にできたこと）

- [x] intent / want スキーマ
- [x] wants 抽出 YAML（grok / muse）
- [x] bronze wants.jsonl / sessions.jsonl
- [x] kaggle-bqml-core / ml-repos-analyze テンプレ作成
- [x] CI

---

## ID 修正メモ

- `INTENT-2026-11-11-02_session-wants-baseline` → **INTENT-03** に採番し直し（02 と衝突していた）
- 旧ファイルは削除し、`INTENT-2026-11-11-03_session-wants-baseline.yaml` を正とする
