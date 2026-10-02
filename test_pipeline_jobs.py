import json
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app, _save_pipeline_job, _load_pipeline_job


def test_pipeline_job_state_persists(tmp_path, monkeypatch):
    import app.main as m
    monkeypatch.setattr(m, 'ARTIFACT_ROOT', tmp_path)
    state = _save_pipeline_job('persist-test', status='failed', stage='STT', progress=40,
                               completed_stages=['PREPARE', 'EXTRACT_AUDIO'], upload_id='u1',
                               source_language='en', target_language='ar')
    assert state['stage'] == 'STT'
    m.PIPELINE_JOBS.pop('persist-test', None)
    loaded = _load_pipeline_job('persist-test')
    assert loaded['completed_stages'] == ['PREPARE', 'EXTRACT_AUDIO']
    assert json.loads((tmp_path / 'pipeline-persist-test' / 'job.json').read_text())['progress'] == 40


def test_pipeline_status_not_found():
    client = TestClient(app)
    response = client.get('/v1/pipeline-jobs/not-real', headers={'Authorization': 'Bearer ' + __import__('app.main', fromlist=['_make_token'])._make_token('test','test@example.com')})
    assert response.status_code == 404
