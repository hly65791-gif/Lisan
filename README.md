# Lisan Backend

Minimal production-oriented API contract for Lisan processing.

## Run

```bash
cd backend
python -m venv .venv
# activate the environment
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Endpoints

- `GET /health`
- `POST /v1/transcribe`
- `POST /v1/translate`
- `POST /v1/ocr`

The API intentionally returns `501` when a real provider is not configured. It never fabricates a transcript, translation, or OCR result.

## Rendering

`POST /v1/render` and `POST /v1/render-upload` burn the translated subtitles into the video with FFmpeg/libass using the **Lisan Classic** visual style. The style is intentionally matched to the supplied reference: bold white Arabic text, strong black outline, subtle shadow, centered at the bottom, with the original video geometry preserved (including existing black bars). Arabic shaping/RTL layout is handled by libass. The rendered MP4 is validated with ffprobe and stored as a persistent artifact.


## Media delivery v0.2
Large source videos use resumable uploads:
- `POST /v1/uploads/init`
- `GET /v1/uploads/{id}`
- `PUT /v1/uploads/{id}` with `X-Chunk-Offset` and `X-Total-Size`
- `POST /v1/uploads/{id}/complete`
- `POST /v1/render-upload`
- `GET /v1/artifacts/{id}`
- `GET /v1/artifacts/{id}/download`

The default storage directory is `LISAN_DATA_DIR` (default `/tmp/lisan-data`). For production, replace local disk with object storage and signed URLs.

### Lisan Classic subtitle style

- Font: Noto Sans Arabic
- Weight: bold
- Text: white
- Outline: black, strong 4px ASS outline
- Shadow: subtle black shadow
- Position: bottom-center
- Margins: 70px left/right, 55px bottom on a 1920x1080 subtitle canvas
- No subtitle background box
- Original video aspect ratio/geometry is preserved
- Arabic/RTL shaping is performed by libass

The app currently uses this style as the default burn-in style so exported videos have a consistent Lisan look.

### Render validation and smoke testing
Every successful render response includes a `validation` object. The backend rejects a render when the output is empty, has no video stream, loses required audio, changes source dimensions, has non-positive/invalid metadata, or drifts beyond the configured duration tolerance.

The backend test suite includes a real FFmpeg smoke test (`backend/tests/test_render_e2e.py`) that generates a small video+audio fixture, burns Arabic SRT subtitles, and independently probes the resulting MP4 with ffprobe.
