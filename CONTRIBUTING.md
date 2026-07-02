# Contributing to Crucible

Thanks for your interest in improving Crucible! This repo is a Claude Code plugin
**marketplace** (`crucible`) whose flagship plugin is **`crucible-rdd`**. Contributions
of all kinds are welcome — bug reports, skill improvements, MCP-server features, docs.

## Repository layout

```text
crucible/
├── .claude-plugin/marketplace.json   # marketplace catalog
├── plugins/
│   └── crucible-rdd/                  # the plugin
│       ├── .claude-plugin/plugin.json
│       ├── skills/                    # the five crucible:* skills (Markdown)
│       └── mcp-server/                # optional Python MCP server
├── docs/                             # deeper documentation
└── scripts/                          # maintenance scripts (e.g. version bump)
```

The skills are **skills-primary**: they work standalone by reading/writing `.crucible/`
files, and transparently delegate to the MCP server when it's available.

## Dev setup (MCP server)

You need [`uv`](https://docs.astral.sh/uv/) on your `PATH`.

```bash
cd plugins/crucible-rdd/mcp-server
uv sync --extra dev        # install runtime + dev dependencies
```

## Quality gates

All of these run in CI on every push/PR — please run them locally first:

```bash
cd plugins/crucible-rdd/mcp-server
uv run --extra dev ruff check           # lint
uv run --extra dev ruff format          # auto-format
uv run --extra dev mypy src             # type-check
uv run --extra dev python -m pytest -q  # tests
```

Optional but recommended — install the git hooks so this happens automatically:

```bash
pipx install pre-commit && pre-commit install
```

## Making changes

- **Skills** live in `plugins/crucible-rdd/skills/*.md`. Keep the dual MCP/file-mode
  behaviour (each skill starts with a "Step 0: Check for MCP" block).
- **MCP server** code lives in `plugins/crucible-rdd/mcp-server/src/crucible/`. Add or
  update tests under `tests/` for any behavioural change.
- Keep changes small and focused. One logical change per PR.

## Submitting a PR

1. Fork and branch from `main`.
2. Make your change; ensure all quality gates pass.
3. Add a `CHANGELOG.md` entry under `## [Unreleased]`.
4. Open a PR using the template. Link any related issue.

## Releasing (maintainers)

See the release rhythm in [`CHANGELOG.md`](CHANGELOG.md) and use
[`scripts/bump-version.sh`](scripts/bump-version.sh) to bump the version across
`plugin.json` and `marketplace.json`, then tag and cut a GitHub Release.
