# Crucible

A Claude Code **plugin marketplace** for Review-driven Development (RDD) of AI/ML
research. Add the marketplace once, then install whichever plugins you want.

## Install

```text
/plugin marketplace add vasanthsarathy/crucible
/plugin install crucible-rdd@crucible
```

Then `/reload-plugins` (or restart Claude Code) to activate.

## Plugins

| Plugin | Description |
| --- | --- |
| [`crucible-rdd`](plugins/crucible-rdd/) | Run your research work through an adversarial reviewer panel at every stage. Skills-primary: works standalone, enriched by an optional MCP server. |

_More plugins coming._

## Updating

Plugin updates ship as version bumps in each plugin's `plugin.json`. To pull the
latest:

```text
/plugin marketplace update crucible
```

## Repository layout

```text
crucible/                         ← this marketplace
├── .claude-plugin/
│   └── marketplace.json          ← catalog of plugins
└── plugins/
    └── crucible-rdd/             ← the RDD plugin (its own README, skills, MCP server)
```
