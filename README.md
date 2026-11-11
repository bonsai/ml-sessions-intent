# ml-sessions-intent

ML session intents & structured wants.

**Author note**: Scaffold + first structured extraction by Grok (xAI) — 2026-11-11

---

## Two layers

| Layer | Path | Role |
|-------|------|------|
| **Intent** | `intents/` | Experiment-sized unit (goal → next_action → artifacts) |
| **Want** | `wants/` | Session-extracted やりたいこと with **濃さ / 関連 / 依存 / 学習** |

Want が先にあり、そこから Intent に落とす、という流れを想定。

---

## Want の構造

```yaml
id: W-...
title: ...
intensity: 0.0–1.0   # 濃さ
cluster: agents | ml-data | meta-process | ...
related: [...]       # 関連
depends_on: [...]    # 依存（これより先に進めるもの）
enables: [...]       # これが進むと開けるもの
learning: |          # この want から見たパターン・教訓
  ...
```

---

## 今日の抽出サマリー (2026-11-11 Grok)

| ID | Title | 濃さ |
|----|-------|------|
| W-20261111-06 | やりたいことを構造化（濃さ・関連・依存・学習） | 0.95 |
| W-20261111-02 | Kaggleで実践MLを始めたい | 0.90 |
| W-20261111-01 | Muse系エージェント全体像 | 0.85 |
| W-20261111-03 | BQMLをKaggleで再現 | 0.80 |
| W-20261111-04 | 共通基盤テンプレをrepo化 | 0.75 (done) |
| W-20261111-05 | セッション構造化・過去intent救出 | 0.70 |

学習で見えた型:
- structure-before-execution
- free-compute-first
- agent-router-as-backbone
- session-as-memory

詳細: `wants/2026-11-11-grok.yaml`

---

## Layout

```
intents/          # experiment units
wants/            # per-session structured やりたいこと
schema/
src/ml_sessions_intent/
notebooks/
```
