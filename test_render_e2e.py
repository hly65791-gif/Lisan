import importlib.util
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("lisan_backend", ROOT / "app" / "main.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def _ffmpeg_available():
    return shutil.which("ffmpeg") and shutil.which("ffprobe")


@pytest.mark.skipif(not _ffmpeg_available(), reason="ffmpeg/ffprobe not installed")
def test_real_ffmpeg_render_smoke(tmp_path):
    source = tmp_path / "source.mp4"
    srt = tmp_path / "translated.srt"
    output = tmp_path / "translated_video.mp4"

    # Small deterministic fixture: video + audio, so the real render path is exercised.
    subprocess.run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-f", "lavfi", "-i", "testsrc=size=640x360:rate=25",
        "-f", "lavfi", "-i", "sine=frequency=880:sample_rate=44100",
        "-t", "2", "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-shortest", str(source),
    ], check=True)
    srt.write_text(
        "1\n00:00:00,300 --> 00:00:01,500\nمرحباً بكم في لسان\n",
        encoding="utf-8",
    )

    result = module._render(source, srt, output, "LISAN_CLASSIC", 54, "BOTTOM", "OUTLINE", 4, 1, 50, 88)

    assert result["validation"]["valid"] is True
    assert result["has_video"] is True
    assert result["has_audio"] is True
    assert result["width"] == 640
    assert result["height"] == 360
    assert output.exists() and output.stat().st_size > 0

    # Independent ffprobe check: do not rely only on the backend's parsed result.
    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_type", "-of", "json", str(output)],
        check=True, capture_output=True, text=True,
    )
    assert '"codec_type": "video"' in probe.stdout
    assert '"codec_type": "audio"' in probe.stdout
