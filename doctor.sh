#!/usr/bin/env bash
set -euo pipefail
ROOT="${1:-.}"
cd "$ROOT"
pass(){ echo "PASS: $1"; }
warn(){ echo "WARN: $1"; }
fail(){ echo "FAIL: $1"; }
command -v java >/dev/null 2>&1 && pass "Java: $(java -version 2>&1 | head -1)" || fail "Java not found"
[ -n "${JAVA_HOME:-}" ] && pass "JAVA_HOME=$JAVA_HOME" || warn "JAVA_HOME not set"
[ -x ./gradlew ] && pass "gradlew executable" || fail "gradlew missing/not executable"
[ -f ./gradlew.bat ] && pass "gradlew.bat present" || warn "gradlew.bat missing"
[ -f ./gradle/wrapper/gradle-wrapper.jar ] && pass "Gradle Wrapper JAR present" || fail "Gradle Wrapper JAR missing"
[ -f ./gradle/wrapper/gradle-wrapper.properties ] && pass "Wrapper properties present" || fail "Wrapper properties missing"
[ -n "${ANDROID_HOME:-${ANDROID_SDK_ROOT:-}}" ] && pass "Android SDK env present" || warn "Android SDK env not set"
command -v adb >/dev/null 2>&1 && pass "adb available" || warn "adb not available"
command -v gradle >/dev/null 2>&1 && pass "system Gradle: $(gradle --version | grep '^Gradle ' | head -1)" || warn "system Gradle not installed (Wrapper is preferred)"
