#!/usr/bin/env bash
set -u
echo "LISAN BUILD DOCTOR"
echo "=================="
echo "Project: $(basename "$(pwd)")"
echo

if [[ -x "./gradlew" ]]; then
  echo "Wrapper: PASS (./gradlew)"
elif [[ -f "./gradlew" || -f "./gradlew.bat" ]]; then
  echo "Wrapper: INCOMPLETE"
else
  echo "Wrapper: MISSING"
fi

if command -v java >/dev/null 2>&1; then
  echo "JDK: $(java -version 2>&1 | head -1)"
else
  echo "JDK: MISSING"
fi

if command -v gradle >/dev/null 2>&1; then
  echo "System Gradle: $(gradle --version | awk '/Gradle /{print $2; exit}')"
else
  echo "System Gradle: MISSING"
fi

if [[ -n "${ANDROID_HOME:-}" && -d "${ANDROID_HOME}" ]]; then
  echo "Android SDK: PASS ($ANDROID_HOME)"
elif [[ -n "${ANDROID_SDK_ROOT:-}" && -d "${ANDROID_SDK_ROOT}" ]]; then
  echo "Android SDK: PASS ($ANDROID_SDK_ROOT)"
else
  echo "Android SDK: MISSING"
fi

if command -v adb >/dev/null 2>&1; then
  echo "ADB: PASS"
else
  echo "ADB: MISSING"
fi

if command -v ffmpeg >/dev/null 2>&1; then
  echo "FFmpeg: PASS"
else
  echo "FFmpeg: MISSING"
fi

if command -v ffprobe >/dev/null 2>&1; then
  echo "ffprobe: PASS"
else
  echo "ffprobe: MISSING"
fi
