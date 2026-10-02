# Lisan v0.26 Distributed Queue

Lisan supports two execution modes:

- `LISAN_QUEUE_BACKEND=inprocess`: local ThreadPoolExecutor fallback for development.
- `LISAN_QUEUE_BACKEND=redis`: Redis Streams queue shared by multiple backend instances.

## Production requirements

1. Run Redis and set `LISAN_REDIS_URL`.
2. Set the same `LISAN_REDIS_STREAM` and `LISAN_REDIS_GROUP` on all API/worker instances.
3. Put `LISAN_DATA_DIR` on shared persistent storage accessible by every worker, because uploaded media and artifacts are files.
4. Scale backend instances horizontally; Redis Streams distributes jobs among consumers in the group.

The API remains responsive while STT/OCR/FFmpeg work runs in workers. Job state continues to be checkpointed to disk. Redis is optional and the default remains the local queue.

### Failure semantics

Jobs persist their own `failed` state and are acknowledged after the worker finishes. A future production hardening step is automatic reclaim of abandoned Redis pending entries after worker crashes; do not treat the current queue as an exactly-once guarantee.
