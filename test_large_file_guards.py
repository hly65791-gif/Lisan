import io
from pathlib import Path
from fastapi import UploadFile
from fastapi import HTTPException
from app.main import _stream_to_file, MAX_INPUT_BYTES, OCR_MAX_FRAMES


def test_stream_copy_is_chunked_and_bounded(tmp_path: Path):
    upload = UploadFile(filename="sample.mp4", file=io.BytesIO(b"x" * 5000))
    target = tmp_path / "sample.mp4"
    size = _stream_to_file(upload, target, max_bytes=6000)
    assert size == 5000
    assert target.stat().st_size == 5000


def test_stream_copy_rejects_over_limit(tmp_path: Path):
    upload = UploadFile(filename="large.mp4", file=io.BytesIO(b"x" * 5001))
    target = tmp_path / "large.mp4"
    try:
        _stream_to_file(upload, target, max_bytes=5000)
    except HTTPException as exc:
        assert exc.status_code == 413
        assert exc.detail == "INPUT_FILE_TOO_LARGE"
    else:
        raise AssertionError("expected 413")


def test_large_file_defaults_are_explicit():
    assert MAX_INPUT_BYTES >= 4 * 1024 * 1024 * 1024
    assert OCR_MAX_FRAMES > 0
