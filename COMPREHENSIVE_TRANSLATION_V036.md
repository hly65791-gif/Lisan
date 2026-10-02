# Lisan v0.36 — Comprehensive Translation

The video setup screen now exposes an optional **ترجمة شاملة** switch.

When enabled, Lisan includes visible on-screen text (OCR) in addition to spoken subtitles. A nested **استبدال النص الأصلي** option controls whether detected OCR text is marked for replacement during final rendering.

Settings are persisted per project in Room via migration 7→8:
- `comprehensiveTranslation`
- `replaceOcrText`

If comprehensive translation is disabled, OCR replacement is never enabled by the worker. Motion tracking metadata is enabled for OCR overlays only when comprehensive translation is selected.
