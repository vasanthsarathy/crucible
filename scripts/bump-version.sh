#!/usr/bin/env bash
#
# Bump the crucible-rdd plugin version in lockstep across:
#   - plugins/crucible-rdd/.claude-plugin/plugin.json
#   - .claude-plugin/marketplace.json  (the crucible-rdd entry)
#
# Usage:  scripts/bump-version.sh <major.minor.patch>
# Example: scripts/bump-version.sh 0.2.0
#
# Requires GNU sed (available in Git Bash on Windows, and on Linux/macOS-with-gsed).
set -euo pipefail

NEW="${1:-}"
if [[ ! "$NEW" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  echo "usage: $(basename "$0") <major.minor.patch>   e.g. $(basename "$0") 0.2.0" >&2
  exit 1
fi

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PLUGIN_JSON="$ROOT/plugins/crucible-rdd/.claude-plugin/plugin.json"
MARKET_JSON="$ROOT/.claude-plugin/marketplace.json"

for f in "$PLUGIN_JSON" "$MARKET_JSON"; do
  # Replace only the first "version": "x.y.z" occurrence in each file.
  sed -i -E "0,/\"version\": \"[0-9]+\.[0-9]+\.[0-9]+\"/ s//\"version\": \"$NEW\"/" "$f"
  echo "updated ${f#"$ROOT/"}"
done

cat <<EOF

version bumped to $NEW. Next steps:
  1. Add a CHANGELOG.md entry under a new '## [$NEW]' heading.
  2. git commit -am "Release v$NEW"
  3. git tag -a "v$NEW" -m "crucible-rdd v$NEW"
  4. git push origin main "v$NEW"
  5. gh release create "v$NEW" --title "v$NEW" --notes "..."
EOF
