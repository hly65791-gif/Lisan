#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../../../../.." && pwd)"
VERSION="${GRADLE_VERSION:-8.10.2}"
BIN="$ROOT/.app-builder/gradle/gradle-$VERSION/bin/gradle"
if [ ! -x "$BIN" ]; then
  echo "Gradle runtime not provisioned. Run: bash .claude/skills/app-builder/tools/gradle/bootstrap-gradle.sh ." >&2
  exit 20
fi
exec "$BIN" "$@"
