from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app, RENDER_JOBS, _set_job


def test_render_job_status_not_found():
    client = TestClient(app)
    response = client.get('/v1/render-jobs/missing-job', headers={'Authorization': 'Bearer ' + __import__('app.main', fromlist=['_make_token'])._make_token('test','test@example.com')})
    assert response.status_code == 404


def test_render_job_status_round_trip():
    _set_job('test-job', status='running', progress=42, artifact_id='artifact', owner_id='test')
    client = TestClient(app)
    response = client.get('/v1/render-jobs/test-job', headers={'Authorization': 'Bearer ' + __import__('app.main', fromlist=['_make_token'])._make_token('test','test@example.com')})
    assert response.status_code == 200
    body = response.json()
    assert body['status'] == 'running'
    assert body['progress'] == 42
    assert body['artifact_id'] == 'artifact'
    RENDER_JOBS.pop('test-job', None)


def test_job_worker_count_is_positive():
    from app.main import JOB_WORKERS
    assert JOB_WORKERS > 0
