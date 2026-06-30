# Restructure into a multi-plugin marketplace

## Plan (proposed — awaiting verification)

Goal: turn the repo into the **`crucible` marketplace** holding named plugins,
starting with the flagship **`crucible-rdd`**, leaving room for `captain-research`.

Scope guardrail: only the plugin's *install identity* changes. KEEP all internal
branding — Python pkg `crucible`, MCP server name, `CRUCIBLE_DIR`, `.crucible/`
state dir, skill names. No second full rename.

- [ ] Create `plugins/crucible-rdd/` and move the plugin into it:
      `skills/`, `mcp-server/`, `README.md`, `.claude-plugin/plugin.json`
- [ ] In moved `plugin.json`: change `name` "crucible" → "crucible-rdd"
      (leave version, mcpServers key "crucible", env, skills paths as-is —
      `${CLAUDE_PLUGIN_ROOT}/mcp-server` still resolves correctly post-move)
- [ ] Create root `.claude-plugin/marketplace.json` (name "crucible") listing
      crucible-rdd with `source: "./plugins/crucible-rdd"`
- [ ] Keep `.gitignore` at repo root (paths still match)
- [ ] Add a short root `README.md` describing the marketplace + install commands
- [ ] Verify: skill files + mcp-server land correctly; `uv run` path intact
- [ ] git add/commit/push
- [ ] (Later, separate task) scaffold `plugins/captain-research/` when ready

All steps above completed and verified.

## Review

Restructured the repo from a single root-level plugin into the **`crucible`
marketplace** holding named plugins.

- Moved the plugin into `plugins/crucible-rdd/` via `git mv` (rename history
  preserved); gitignored `.venv` left behind and cleaned up.
- `plugin.json` `name`: `crucible` → `crucible-rdd` (install identity only —
  all internal branding kept: package `crucible`, MCP server name, `CRUCIBLE_DIR`,
  `.crucible/`, skill names).
- Added root `.claude-plugin/marketplace.json` (name `crucible`) cataloging
  `crucible-rdd` at `./plugins/crucible-rdd`.
- New root `README.md` documents the marketplace + install/update commands;
  detailed plugin README travels with the plugin.
- Verified: both manifests valid JSON; `uv` re-synced the venv at the new path
  and **25/25 tests pass**, confirming `${CLAUDE_PLUGIN_ROOT}/mcp-server` resolves.

Install: `/plugin marketplace add vasanthsarathy/crucible` →
`/plugin install crucible-rdd@crucible`. Future plugins (e.g. `captain-research`)
slot in as a new `plugins/<name>/` folder plus one catalog entry.

---

# Rename hal-research → crucible + GitHub setup

## Plan (approved: Crucible / full rename / private repo)

- [x] Move Python package `src/hal_research/` → `src/crucible/`
- [x] Replace identifiers across all files (MCP tool prefix, package/module,
      plugin & server name, `HAL_RESEARCH_DIR` → `CRUCIBLE_DIR`, `.hal-research`
      → `.crucible`, `research:` command prefix → `crucible:`)
- [x] Rename skill files `research-*.md` → `crucible-*.md`; update plugin.json
- [x] Update author (godbehera → vasanthsarathy)
- [x] Fix cross-platform MCP launch (`uv run` instead of unix-only venv path)
- [x] Add root `.gitignore`
- [x] Re-run pytest (25 passing on the renamed package)
- [x] git init + first commit
- [x] Create private GitHub repo and push
- [ ] Rename local folder hal-research → crucible (optional, see review)

## Review

**Plugin assessment:** The plugin is well-built. Coherent Review-driven
Development design (adversarial reviewer gates + Socratic understanding probes
that block stage advancement), clean skills-primary architecture with
transparent flat-file fallback when the MCP server is absent, consistent persona
naming across README/server/skills, and a passing test suite (25/25).

**Changes made:**
- Full rename `hal-research` → `crucible` (titled "Crucible"): Python package
  `hal_research` → `crucible`, MCP tool prefix `mrc_hal_research_*` → `crucible_*`,
  env var `HAL_RESEARCH_DIR` → `CRUCIBLE_DIR`, runtime state dir `.hal-research`
  → `.crucible`, slash-command namespace `research:*` → `crucible:*`, and all five
  skill files renamed. README title and prose updated.
- Fixed a real cross-platform bug: `plugin.json` and the README hard-coded the
  unix-only `.venv/bin/crucible` path. Switched to `uv run --project ... crucible`,
  which works on Windows/macOS/Linux.
- Set `author` to vasanthsarathy <vsarathy@gmail.com> (was "godbehera").
- Added `.gitignore` (`.venv/`, `__pycache__/`, `.pytest_cache/`, `.crucible/`,
  `.claude/settings.local.json`, OS/editor cruft). Removed the previously
  committed `.pytest_cache`.
- Regenerated `uv.lock` for the new package name.

**Encoding note:** an intermediate bulk-edit pass wrote files as UTF-8-with-BOM
via PowerShell, mangling box-drawing/arrow characters in the README, skills, and
server comments. Detected and reversed losslessly (Windows-1252 → original UTF-8
bytes); all Unicode now renders correctly.

**Local folder:** the on-disk folder is still `...\plugins\hal-research`; the
GitHub repo is named `crucible`. Renaming the local folder is safe but must happen
outside a shell rooted in it (Windows locks the cwd), so it's left as a manual
step — it does not affect the plugin or the remote.
