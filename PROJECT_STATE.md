# Lisan v0.43.2 — Project State

## Current focus
Release hardening, reproducible Android builds, and production provider readiness.

## Verified in v0.43.1
- Android modular Clean Architecture foundation.
- Room database with migrations through schema version 8.
- Persistent processing-job state.
- Provider interfaces for STT, translation, and OCR.
- Backend client for resumable uploads, pipeline jobs, render jobs, artifact download, and resume.
- Backend authentication and per-resource ownership.
- Resumable uploads and configurable local/GCS/S3 object storage.
- Optional Redis Streams queue with in-process development fallback.
- OCR detection and automatic motion tracking.
- FFmpeg/libass subtitle rendering and render validation.
- Subtitle editor, SRT/VTT export, styling, alignment/karaoke support.
- Comprehensive translation and OCR replacement settings.
- Backend Python compile: PASS.
- Backend tests: 48/48 PASS (0 warnings after FastAPI lifespan migration).
- ZIP integrity: PASS.
- FFmpeg and ffprobe are available in the inspection environment.

## Current blockers
- Android Gradle Wrapper is absent from the supplied archive.
- No system Gradle executable is available in the inspection environment.
- Android SDK/ADB are not available in the inspection environment.
- Therefore Android compilation, lint, APK, and AAB remain UNVERIFIED/BLOCKED.

## Provider readiness
- Android provider abstractions are implemented.
- Backend endpoints exist for STT/translation/OCR, but real external AI providers remain configuration-dependent.
- The backend intentionally returns a provider-not-configured response instead of fabricating AI results.

## Release gate
- Backend: PASS (48/48 tests).
- Android build: BLOCKED.
- APK: NOT BUILT / UNVERIFIED.
- AAB: NOT BUILT / UNVERIFIED.
- Production release: BLOCKED until Android build and artifact validation are performed.

## Next action
1. Provision a verified Gradle Wrapper using the project's intended Gradle/AGP compatibility.
2. Build `:app:assembleDebug`.
3. Run Android unit tests and lint.
4. Fix any compile/lint regressions.
5. Build and validate release APK/AAB.
6. Only then perform the final release gate.

## Important rule
Do not claim Android build, APK, AAB, lint, or runtime success until the corresponding command/artifact has been actually verified.
