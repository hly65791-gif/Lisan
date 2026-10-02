# Lisan v0.24 — Render Job Queue

Heavy FFmpeg rendering is now executed through an in-process bounded worker pool instead of blocking the HTTP request.

## Flow
1. Android uploads/resumes the source video.
2. `POST /v1/render-upload/async` stores subtitle inputs and returns `job_id` immediately.
3. A background render worker executes FFmpeg and final validation.
4. Android polls `GET /v1/render-jobs/{job_id}`.
5. Only a `completed` job with a valid render result can reach `COMPLETED` on Android.

## Configuration
- `LISAN_JOB_WORKERS` — number of concurrent render workers (default: 2).
- `LISAN_DATA_DIR` — persistent data root.

This is intentionally an in-process queue for the current deployment. For multi-instance production deployment, the same job contract should be backed by Redis/RQ, Celery, Cloud Tasks, or another durable queue.
