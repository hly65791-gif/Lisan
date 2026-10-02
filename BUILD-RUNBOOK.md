# App Builder Build Runbook

## Android
1. Run `tools/gradle/doctor.sh <project>`.
2. If Wrapper is missing, run the bootstrap tool from `tools/gradle/`.
3. Use `./gradlew --version`.
4. Run `./gradlew test`.
5. Run `./gradlew assembleDebug` for a debug artifact.
6. Run `./gradlew assembleRelease` only when release signing/configuration is intentionally available.
7. Verify APK/AAB artifacts before reporting success.

## Backend
1. Run syntax/import checks.
2. Run unit/API tests.
3. Build the Docker image.
4. Run the container health endpoint.
5. Verify required external providers are configured without printing secrets.

## Rule
A generated command is not a build result. Only command output from an actual run can establish PASS.
