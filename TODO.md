# Lisan TODO — v0.43.1

## P0 — Android build baseline
- [ ] Provision complete Gradle Wrapper.
- [ ] Verify JDK/Gradle/AGP/Kotlin compatibility.
- [ ] Verify Android SDK 35 and required build tools.
- [ ] Run `:app:assembleDebug`.
- [ ] Run Android unit tests.
- [ ] Run lint.

## P1 — Release hardening
- [ ] Verify release signing configuration without committing secrets.
- [ ] Build release APK.
- [ ] Build release AAB.
- [ ] Inspect package/version/signing/artifact metadata.
- [ ] Run critical-path smoke tests on a real Android device/emulator.

## P2 — Production AI providers
- [ ] Configure real STT provider.
- [ ] Configure real translation provider.
- [ ] Configure real OCR provider.
- [ ] Add provider health/configuration diagnostics.
- [ ] Validate timeout/retry/error behavior against real providers.

## P3 — Production infrastructure
- [ ] Choose and configure object storage.
- [ ] Configure Redis Streams for multi-instance workers if required.
- [ ] Configure private storage and short-lived signed URLs.
- [ ] Configure retention/lifecycle policies.
- [ ] Configure HTTPS and production authentication secret.

## P4 — Product completion
- [ ] Complete notifications/profile/settings navigation gaps.
- [ ] Verify pause/resume behavior after network interruption.
- [ ] Verify large-file behavior against configured limits.
- [ ] Verify comprehensive OCR replacement and motion tracking end-to-end.
