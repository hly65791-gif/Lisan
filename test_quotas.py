import os
os.environ.setdefault("LISAN_AUTH_REQUIRED", "true")
from fastapi.testclient import TestClient
from app.main import app, _load_users, _save_users, QUOTA_MONTHLY_MINUTES, QUOTA_MAX_VIDEO_SECONDS


def test_usage_endpoint_and_new_account_defaults(tmp_path, monkeypatch):
    monkeypatch.setattr("app.main.AUTH_DB", tmp_path / "users.json")
    client=TestClient(app)
    email="quota@example.com"
    r=client.post("/v1/auth/register", data={"email":email,"password":"strongpass123"})
    assert r.status_code==200
    token=r.json()["access_token"]
    r=client.get("/v1/account/usage", headers={"Authorization":f"Bearer {token}"})
    assert r.status_code==200
    body=r.json()
    assert body["plan"]=="free"
    assert body["translation_minutes_limit"]==QUOTA_MONTHLY_MINUTES
    assert body["max_video_seconds"]==QUOTA_MAX_VIDEO_SECONDS
    assert body["translation_minutes_used"]==0


def test_translation_reservation_blocks_over_quota(monkeypatch, tmp_path):
    import app.main as m
    monkeypatch.setattr(m, "AUTH_DB", tmp_path / "users.json")
    monkeypatch.setattr(m, "QUOTA_MONTHLY_MINUTES", 1)
    email="reserve@example.com"
    client=TestClient(m.app)
    token=client.post("/v1/auth/register", data={"email":email,"password":"strongpass123"}).json()["access_token"]
    user=client.get("/v1/auth/me", headers={"Authorization":f"Bearer {token}"}).json()
    m._reserve_translation(user["user_id"], 50)
    try:
        try:
            m._reserve_translation(user["user_id"], 20)
            assert False, "reservation should exceed remaining quota"
        except Exception as exc:
            assert getattr(exc, "status_code", None)==402
    finally:
        m._finalize_translation(user["user_id"], 50, False)
