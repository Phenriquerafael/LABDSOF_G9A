#!/bin/sh
# Fails if the skill mirrors drift from the canonical .agents/skills/.
# Usage: scripts/check-skill-mirrors.sh   (from any directory)
set -u

root=$(cd "$(dirname "$0")/.." && pwd)
canonical="$root/.agents/skills"
status=0

for mirror in .claude/skills .opencode/skills; do
  if ! diff -r "$canonical" "$root/$mirror"; then
    echo "DRIFT: $mirror differs from .agents/skills (copy the canonical files over it)" >&2
    status=1
  fi
done

[ "$status" -eq 0 ] && echo "OK: .claude/skills and .opencode/skills match .agents/skills"
exit "$status"
