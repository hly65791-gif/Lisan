# Lisan v0.43 Release Hardening

- Android versionName: 0.43.0
- Android versionCode: 43
- Release build has minification/shrinking explicitly configured but disabled until a real release build is verified.
- Cleartext HTTP is disabled for release builds.
- Debug builds retain cleartext access for local development backends such as 10.0.2.2:8000.
- Production backend must use HTTPS.
- No signing secrets are stored in the project.

## Current release blocker
The project snapshot does not contain a Gradle Wrapper and this environment has no Android SDK/Gradle installation, so APK/AAB generation is not claimed.
