#!/usr/bin/env bash
set -euo pipefail

PROJECT="${1:-.}"
GRADLE_VERSION="${GRADLE_VERSION:-8.10.2}"
HOST="https://services.gradle.org/distributions"
ROOT="$(cd "$PROJECT" && pwd)"
WRAPPER_DIR="$ROOT/gradle/wrapper"
TOOLS_DIR="$ROOT/.app-builder/gradle"
DIST_DIR="$TOOLS_DIR/gradle-$GRADLE_VERSION"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

command -v java >/dev/null 2>&1 || { echo "GRADLE_BOOTSTRAP_BLOCKED: Java is required" >&2; exit 20; }
command -v curl >/dev/null 2>&1 || { echo "GRADLE_BOOTSTRAP_BLOCKED: curl is required" >&2; exit 20; }
command -v unzip >/dev/null 2>&1 || { echo "GRADLE_BOOTSTRAP_BLOCKED: unzip is required" >&2; exit 20; }

mkdir -p "$WRAPPER_DIR" "$TOOLS_DIR"
JAR="$TMP/gradle-wrapper.jar"
SUM="$TMP/gradle-wrapper.jar.sha256"
ZIP="$TMP/gradle-$GRADLE_VERSION-bin.zip"
ZIP_SUM="$TMP/gradle-$GRADLE_VERSION-bin.zip.sha256"

curl -fsSL "$HOST/gradle-$GRADLE_VERSION-wrapper.jar" -o "$JAR"
curl -fsSL "$HOST/gradle-$GRADLE_VERSION-wrapper.jar.sha256" -o "$SUM"
EXPECTED_JAR="$(tr -d '[:space:]' < "$SUM")"
ACTUAL_JAR="$(sha256sum "$JAR" | awk '{print $1}')"
[ "$EXPECTED_JAR" = "$ACTUAL_JAR" ] || { echo "GRADLE_CHECKSUM_FAILED: wrapper JAR" >&2; exit 21; }
cp "$JAR" "$WRAPPER_DIR/gradle-wrapper.jar"

cat > "$WRAPPER_DIR/gradle-wrapper.properties" <<PROPS
distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
distributionUrl=https\\://services.gradle.org/distributions/gradle-$GRADLE_VERSION-bin.zip
networkTimeout=10000
retries=2
validateDistributionUrl=true
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists
PROPS

curl -fsSL "$HOST/gradle-$GRADLE_VERSION-bin.zip" -o "$ZIP"
curl -fsSL "$HOST/gradle-$GRADLE_VERSION-bin.zip.sha256" -o "$ZIP_SUM"
EXPECTED_ZIP="$(tr -d '[:space:]' < "$ZIP_SUM")"
ACTUAL_ZIP="$(sha256sum "$ZIP" | awk '{print $1}')"
[ "$EXPECTED_ZIP" = "$ACTUAL_ZIP" ] || { echo "GRADLE_CHECKSUM_FAILED: Gradle distribution" >&2; exit 21; }

rm -rf "$DIST_DIR"
unzip -q "$ZIP" -d "$TOOLS_DIR"

# Use the standard wrapper scripts if they are not already present.
if [ ! -f "$ROOT/gradlew" ]; then
  cat > "$ROOT/gradlew" <<'SCRIPT'
#!/bin/sh
APP_HOME=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd -P)
CLASSPATH=$APP_HOME/gradle/wrapper/gradle-wrapper.jar
exec java -classpath "$CLASSPATH" org.gradle.wrapper.GradleWrapperMain "$@"
SCRIPT
  chmod +x "$ROOT/gradlew"
fi

if [ ! -f "$ROOT/gradlew.bat" ]; then
  cat > "$ROOT/gradlew.bat" <<'BAT'
@echo off
set DIR=%~dp0
java -classpath "%DIR%gradle\wrapper\gradle-wrapper.jar" org.gradle.wrapper.GradleWrapperMain %*
BAT
fi

"$DIST_DIR/bin/gradle" --version
printf 'GRADLE_BOOTSTRAPPED\n'
printf 'Gradle: %s\n' "$GRADLE_VERSION"
printf 'Wrapper JAR SHA-256: %s\n' "$ACTUAL_JAR"
printf 'Distribution SHA-256: %s\n' "$ACTUAL_ZIP"
