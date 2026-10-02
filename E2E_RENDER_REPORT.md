# Lisan Render E2E Report — v0.21.0

## Real manual render
A real 4-second MP4 fixture was rendered through the backend `_render` path with Arabic subtitles:

- Source: H.264 video + AAC audio
- Source dimensions: 1280×720
- Source duration: 4.00 s
- Subtitle: UTF-8 Arabic SRT
- Style: LISAN_CLASSIC

### Result
- Output duration: 4.01 s
- Output size: 149,901 bytes
- Video stream: PASS
- Audio stream: PASS
- Dimensions preserved: PASS (1280×720)
- Duration tolerance: PASS
- Metadata finite/valid: PASS
- Arabic subtitle frame visually inspected: PASS

## Automated regression
`PYTHONPATH=backend pytest -q backend/tests`

**14 passed**

The new E2E test generates its own small video+audio fixture and independently runs ffprobe on the output.

## Build truth
No Android APK/AAB was produced. The available environment still does not provide a complete Android SDK + Gradle toolchain for a verified Android build.
