# Lisan v0.43.1 Build Report

## Inspection environment
- Java: OpenJDK 21.0.11
- System Gradle: NOT FOUND
- Android SDK: NOT FOUND
- ADB: NOT FOUND
- FFmpeg: AVAILABLE
- ffprobe: AVAILABLE
- Gradle Wrapper in archive: MISSING

## Backend validation
- Python compileall: PASS
- Pytest: 48 passed, 12 warnings
- Warnings are FastAPI `on_event` deprecation warnings; they do not fail the test run.

## Android validation
- Gradle build: BLOCKED
- Lint: BLOCKED
- APK: NOT BUILT
- AAB: NOT BUILT

## Release status
BLOCKED — Android toolchain/artifact validation is still required.
