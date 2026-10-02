"""Lisan object storage abstraction.

LOCAL keeps development simple. GCS and S3 are optional production backends.
Objects are addressed by immutable keys and downloaded to a local cache only
when a worker needs a file for FFmpeg/Whisper/OCR.
"""
import os
from pathlib import Path
from typing import Optional

BACKEND = os.getenv("LISAN_STORAGE_BACKEND", "local").strip().lower()
BUCKET = os.getenv("LISAN_STORAGE_BUCKET", "").strip()
PREFIX = os.getenv("LISAN_STORAGE_PREFIX", "lisan").strip("/")

_gcs = None
_s3 = None
if BACKEND == "gcs":
    try:
        from google.cloud import storage as _gcs_module
        _gcs = _gcs_module.Client()
    except Exception:
        _gcs = None
elif BACKEND == "s3":
    try:
        import boto3
        _s3 = boto3.client("s3", endpoint_url=os.getenv("LISAN_S3_ENDPOINT") or None,
                           region_name=os.getenv("AWS_REGION") or None)
    except Exception:
        _s3 = None


def enabled() -> bool:
    return BACKEND == "local" or (BACKEND == "gcs" and _gcs is not None and bool(BUCKET)) or (BACKEND == "s3" and _s3 is not None and bool(BUCKET))


def key(kind: str, identifier: str, filename: str) -> str:
    return f"{PREFIX}/{kind}/{identifier}/{filename}" if PREFIX else f"{kind}/{identifier}/{filename}"


def put_file(path: Path, object_key: str) -> dict:
    if BACKEND == "local":
        return {"backend": "local", "key": object_key}
    if BACKEND == "gcs" and _gcs is not None:
        blob = _gcs.bucket(BUCKET).blob(object_key)
        blob.upload_from_filename(str(path), timeout=600)
        return {"backend": "gcs", "bucket": BUCKET, "key": object_key}
    if BACKEND == "s3" and _s3 is not None:
        _s3.upload_file(str(path), BUCKET, object_key)
        return {"backend": "s3", "bucket": BUCKET, "key": object_key}
    raise RuntimeError("OBJECT_STORAGE_NOT_CONFIGURED")


def download_file(object_key: str, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if BACKEND == "gcs" and _gcs is not None:
        _gcs.bucket(BUCKET).blob(object_key).download_to_filename(str(destination), timeout=600)
        return
    if BACKEND == "s3" and _s3 is not None:
        _s3.download_file(BUCKET, object_key, str(destination))
        return
    raise RuntimeError("OBJECT_STORAGE_NOT_CONFIGURED")


def signed_url(object_key: str, expires_seconds: int = 900) -> Optional[str]:
    if BACKEND == "gcs" and _gcs is not None:
        blob = _gcs.bucket(BUCKET).blob(object_key)
        return blob.generate_signed_url(version="v4", expiration=expires_seconds, method="GET")
    if BACKEND == "s3" and _s3 is not None:
        return _s3.generate_presigned_url("get_object", Params={"Bucket": BUCKET, "Key": object_key}, ExpiresIn=expires_seconds)
    return None


def delete(object_key: str) -> None:
    if BACKEND == "gcs" and _gcs is not None:
        _gcs.bucket(BUCKET).blob(object_key).delete()
    elif BACKEND == "s3" and _s3 is not None:
        _s3.delete_object(Bucket=BUCKET, Key=object_key)
