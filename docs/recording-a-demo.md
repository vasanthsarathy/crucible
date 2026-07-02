# Recording the demo GIF

The README shows a placeholder where a demo GIF should go
(`assets/demo-placeholder.svg`). To replace it with a real recording:

## What to capture

A short (20–40s) loop that shows the core value:

1. `/crucible:start` → give a one-line seed idea → the Flash + Copernicus
   worthiness check.
2. `/crucible:reviewer-round` → the panel reacting to a draft section.
3. `/crucible:advance` → a gate result + the Socratic probe.

Keep it tight — no long pauses. The point is "reviewers push back," not a full run.

## How to record

Use any terminal recorder:

- **[asciinema](https://asciinema.org/)** + [`agg`](https://github.com/asciinema/agg)
  to render a GIF:
  ```bash
  asciinema rec demo.cast
  # …do the run…
  agg demo.cast assets/demo.gif
  ```
- Or a screen recorder (e.g. ScreenToGif on Windows, Kap on macOS) exporting a GIF.

## Wire it into the README

1. Save the GIF as `assets/demo.gif`.
2. In the root `README.md`, replace the placeholder image source
   `assets/demo-placeholder.svg` with `assets/demo.gif` (and drop the "placeholder"
   caption).

Aim for < 3 MB so it loads fast on the GitHub landing page.
