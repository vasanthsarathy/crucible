# `crucible:reviewer-round`

> Run a full adversarial reviewer panel on your current sections — any time.

## When to use

Whenever you want feedback — **not just at gates**. Early and often is cheaper.

## What it does

Sequentially embodies the nine reviewer personas, each reading the specified
sections through its distinct lens, axis (soundness or significance), and
default stance — including Cicero, a champion voice arguing the strongest honest
case for the work, and Rawls, an ethics and societal-impact voice:

| Reviewer | Lens | Axis | Votes? |
| --- | --- | --- | --- |
| Flash | 60-second scan | significance | ✓ |
| Archimedes | theory & rigor | soundness | ✓ |
| Edison | empirical evidence | soundness | ✓ |
| Copernicus | significance & novelty | significance | ✓ |
| Orwell | clarity & presentation | cross-cutting | ✓ |
| Linnaeus | scholarship & positioning (live search) | cross-cutting | findings only |
| Socrates | assumption auditing | cross-cutting | findings only |
| Cicero | champion — strongest case for the work | significance | findings only |
| Rawls | ethics & societal impact | cross-cutting | findings only |

The round is logged so [`crucible:status`](status.md) and [`crucible:advance`](advance.md)
can reference the latest verdicts.

## Modes

- **MCP:** logs via `crucible_log_review_round`; Linnaeus can use live literature search.
- **File:** appends the round to `review_rounds/`.

## Related

- Gate + advance: [`crucible:advance`](advance.md).
- The full gate threshold is described in [architecture](../architecture.md#the-gate-model).
