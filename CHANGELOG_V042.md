# Lisan v0.42

## End-to-end UX hardening
- Starting a translation now navigates directly to My Projects so the user can monitor progress.
- The selected video is queued before navigation; the unique WorkManager job remains the source of truth.
- Comprehensive Translation now gates OCR processing: OCR is skipped for normal subtitle-only translation to reduce processing cost and time.
- Existing Replace Original Text remains available only when Comprehensive Translation is enabled.

## Validation
- Source-level flow checks performed for VideoPicker → WorkManager → Projects navigation.
- Source-level check confirms OCR is conditional on comprehensiveTranslation.
- Backend test suite inherited from v0.41 remains the regression baseline.
