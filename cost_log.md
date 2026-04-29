# Cost Log (Interim)

| Timestamp (UTC+3) | Bucket | Item | Cost (USD) | Notes |
| :-- | :-- | :-- | --: | :-- |
| 2026-04-29 20:30 | Setup | Local scripting + dataset scaffolding | 0.00 | Local only |
| 2026-04-29 21:10 | Authoring | Seed task generation (offline templates) | 0.00 | No API calls |
| 2026-04-29 21:40 | Validation | Rule evaluator runs | 0.00 | Local Python |
| 2026-04-29 21:50 | Validation | Contamination checks | 0.00 | Local Python |
| 2026-04-29 22:05 | Validation | Inter-rater agreement computation | 0.00 | Local Python |
| 2026-04-29 22:45 | Authoring | 210 raw -> 209 accepted task pipeline pass | 0.00 | Local scripted generation |

## Interim subtotal

- Dataset authoring: **$0.00**
- Training: **$0.00**
- Held-out eval-tier usage: **$0.00**
- Total spent: **$0.00**

## Budget status against week envelope

- Envelope target: $10
- Spent so far: $0
- Remaining: $10

> Note: API-backed generation/judging costs are deferred to post-interim once routing keys and call caps are finalized.
