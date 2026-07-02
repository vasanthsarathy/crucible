# `crucible:reviewer-round`

> Run a full adversarial reviewer panel on your current sections — any time.

## When to use

Whenever you want feedback — **not just at gates**. Early and often is cheaper.

## What it does

Sequentially embodies the seven reviewer personas, each reading the specified
sections through its distinct lens and default-skeptical stance:

| Reviewer | Lens | Votes? |
| --- | --- | --- |
| Flash | 60-second scan | ✓ |
| Archimedes | theory & rigor | ✓ |
| Edison | empirical evidence | ✓ |
| Copernicus | significance & novelty | ✓ |
| Orwell | clarity & presentation | ✓ |
| Linnaeus | scholarship & positioning (live search) | findings only |
| Socrates | assumption auditing | findings only |

The round is logged so [`crucible:status`](status.md) and [`crucible:advance`](advance.md)
can reference the latest verdicts.

## Modes

- **MCP:** logs via `crucible_log_review_round`; Linnaeus can use live literature search.
- **File:** appends the round to `review_rounds/`.

## Related

- Gate + advance: [`crucible:advance`](advance.md).
- The full gate threshold is described in [architecture](../architecture.md#the-gate-model).
