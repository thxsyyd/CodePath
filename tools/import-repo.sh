#!/usr/bin/env bash
# Import another Git repository into a subfolder of this repo, keeping its full commit history.
#
# Usage (run from anywhere inside this repo):
#   tools/import-repo.sh <repo-url-or-path> "<target/folder>" [branch]
#
# Examples:
#   # Start a new project from a course starter repo (instead of forking it)
#   tools/import-repo.sh https://github.com/codepath/ai110-module2show-pawpal-starter "AI110/20260702 W05/Project/pawpal"
#
#   # Move an existing standalone repo into this one
#   tools/import-repo.sh https://github.com/thxsyyd/pawpal "AI110/20260702 W05/Project/pawpal"
#
# Every imported commit keeps its author, date and message; only the file paths
# move into <target/folder>, so commit IDs change. Nothing is pushed: review with
# `git log -- "<target/folder>"`, then push yourself.

set -euo pipefail

if [ $# -lt 2 ]; then
  sed -n '2,16p' "$0" | sed 's/^# \{0,1\}//'
  exit 1
fi

SOURCE="$1"
TARGET="${2%/}"
BRANCH="${3:-}"

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

if [ -n "$(git status --porcelain --untracked-files=no)" ]; then
  echo "Error: commit or stash your changes first." >&2
  exit 1
fi
if [ -n "$(git ls-files -- "$TARGET")" ]; then
  echo "Error: '$TARGET' already contains tracked files." >&2
  exit 1
fi

WORK="$(mktemp -d "${TMPDIR:-/tmp}/import-repo.XXXXXX")"
trap 'rm -rf "$WORK"' EXIT

echo "→ Cloning $SOURCE"
git clone --quiet --no-local "$SOURCE" "$WORK/src"
cd "$WORK/src"
if [ -z "$BRANCH" ]; then
  BRANCH="$(git symbolic-ref --short HEAD)"
fi
git checkout --quiet "$BRANCH"
COUNT="$(git rev-list --count HEAD)"

echo "→ Moving $COUNT commits into '$TARGET/'"
export TARGET
FILTER_BRANCH_SQUELCH_WARNING=1 git filter-branch --force --index-filter '
  git ls-files -s -z |
    perl -0ne "s{\t}{\t\$ENV{TARGET}/}; print" |
    GIT_INDEX_FILE="$GIT_INDEX_FILE.new" git update-index -z --index-info &&
  if [ -f "$GIT_INDEX_FILE.new" ]; then mv "$GIT_INDEX_FILE.new" "$GIT_INDEX_FILE"; fi
' -- "$BRANCH" >/dev/null

cd "$ROOT"
NAME="$(basename "$TARGET")"
git fetch --quiet --no-tags "$WORK/src" "$BRANCH:refs/import/$NAME"
MESSAGE="Import $NAME history into $TARGET"
if [ -n "${IMPORT_TRAILER:-}" ]; then
  MESSAGE="$MESSAGE

$IMPORT_TRAILER"
fi
git merge --quiet --allow-unrelated-histories --no-edit -m "$MESSAGE" "refs/import/$NAME"
git update-ref -d "refs/import/$NAME"

echo "✓ Imported $COUNT commits into '$TARGET/'"
echo "  Check:  git log --oneline -- \"$TARGET\""
