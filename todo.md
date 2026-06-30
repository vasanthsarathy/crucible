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
