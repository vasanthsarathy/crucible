<div align="center">

<img src="assets/banner.svg" alt="Crucible" width="720">

<p>
  <em>Forge your research in fire. Run every stage through a panel of adversarial reviewers —<br>
  you don't advance until the work survives them.</em>
</p>

<p>
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-22c55e"></a>
  <img alt="Version" src="https://img.shields.io/badge/version-0.1.0-3b82f6">
  <img alt="Claude Code plugin" src="https://img.shields.io/badge/Claude%20Code-plugin-8b5cf6?logo=anthropic&logoColor=white">
  <img alt="Skills" src="https://img.shields.io/badge/skills-5-f59e0b">
  <img alt="Built with uv" src="https://img.shields.io/badge/built%20with-uv-de5fe9?logo=python&logoColor=white">
</p>

</div>

---

A Claude Code **plugin marketplace** for Review-Driven Development (RDD) of AI/ML
research. The idea: treat reviewers like tests. Run your work through a panel of
adversarial personas at every stage, the same way TDD runs code through tests —
and don't move on until they pass it *and* you can explain it back without looking
at the draft.

Add the marketplace once, then install whichever plugins you want.

## 📦 Install

```text
/plugin marketplace add vasanthsarathy/crucible
/plugin install crucible-rdd@crucible
```

Then `/reload-plugins` (or restart Claude Code) to activate.

## 🧩 Plugins

| Plugin | What it does |
| :-- | :-- |
| 🔥 [**`crucible-rdd`**](plugins/crucible-rdd/) | Run your research through an adversarial reviewer panel at every stage. Skills-primary — works standalone, enriched by an optional MCP server. |

> _More plugins on the way._ &nbsp;🛰️ A companion plugin is planned and will slot in as a new entry here.

## 🔬 What `crucible-rdd` gives you

<table>
<tr>
<td width="50%" valign="top">

**🚦 Staged gates**

```text
SEED → PROBLEM → SURVEY →
SOLUTION → DEVELOP → PAPER
```

Each gate must be passed by the reviewer panel before you advance — no skipping ahead.

</td>
<td width="50%" valign="top">

**🎭 Seven reviewer personas**

Flash · Archimedes · Edison · Copernicus · Orwell · Linnaeus · Socrates — each with a fixed lens and a default stance built to resist sycophancy.

</td>
</tr>
<tr>
<td valign="top">

**🧠 Socratic probes**

After each gate you answer 2–3 open questions from memory. The stage doesn't advance until you genuinely understand your own work.

</td>
<td valign="top">

**🗂️ Plain-file state**

Everything lives in `.crucible/` as Markdown + JSON. Version-controllable, no server required. The optional MCP server adds live arXiv / Semantic Scholar search.

</td>
</tr>
</table>

➡️ Full details, skill reference, and venue profiles in the
[**plugin README**](plugins/crucible-rdd/README.md).

## 🔄 Updating

Plugin updates ship as version bumps in each plugin's `plugin.json`. To pull the latest:

```text
/plugin marketplace update crucible
```

## 🗂️ Repository layout

```text
crucible/                         ← this marketplace
├── .claude-plugin/
│   └── marketplace.json          ← catalog of plugins
├── assets/
│   └── banner.svg                ← logo
└── plugins/
    └── crucible-rdd/             ← the RDD plugin (its own README, skills, MCP server)
```

## 📄 License

[MIT](LICENSE) © vasanthsarathy

<div align="center">
<sub>🔥 Built for researchers who'd rather get rejected by a robot first.</sub>
</div>
