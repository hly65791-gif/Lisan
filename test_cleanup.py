import json, os, time
from pathlib import Path
from app import cleanup

class DummyStorage:
    BACKEND = "s3"
    def __init__(self): self.deleted=[]
    def delete(self, key): self.deleted.append(key)

def age(path, days):
    t=time.time()-days*86400
    os.utime(path,(t,t))

def test_cleanup_protects_active_and_removes_stale(tmp_path):
    uploads=tmp_path/'uploads'; artifacts=tmp_path/'artifacts'; uploads.mkdir(); artifacts.mkdir()
    active=uploads/'active'; active.mkdir(); (active/'data.part').write_bytes(b'x'); age(active,3)
    stale=uploads/'stale'; stale.mkdir(); (stale/'data.part').write_bytes(b'x'); age(stale,3)
    a=artifacts/'a1'; a.mkdir(); out=a/'translated_video.mp4'; out.write_bytes(b'123');
    (a/'metadata.json').write_text(json.dumps({'storage':{'key':'lisan/artifacts/a1/translated_video.mp4'}})); age(a,31)
    s=DummyStorage()
    result=cleanup.cleanup(tmp_path,uploads,artifacts,{}, {'p':{'status':'running','upload_id':'active'}}, s, False)
    assert 'stale' in result['uploads'] and active.exists() and not stale.exists()
    assert 'a1' in result['artifacts'] and s.deleted==['lisan/artifacts/a1/translated_video.mp4']

def test_cleanup_dry_run_does_not_delete(tmp_path):
    uploads=tmp_path/'uploads'; artifacts=tmp_path/'artifacts'; uploads.mkdir(); artifacts.mkdir()
    d=uploads/'old'; d.mkdir(); (d/'data.part').write_bytes(b'x'); age(d,3)
    result=cleanup.cleanup(tmp_path,uploads,artifacts,{}, {}, None, True)
    assert 'old' in result['uploads'] and d.exists()
