from pathlib import Path
import pytest
from app.main import _auto_track_ocr_overlay

def test_tracking_has_confidence_and_recovery_metadata(tmp_path):
    cv2 = pytest.importorskip('cv2')
    import numpy as np
    video=tmp_path/'recover.mp4'; w,h=320,180
    wr=cv2.VideoWriter(str(video),cv2.VideoWriter_fourcc(*'mp4v'),10,(w,h))
    for i in range(24):
        frame=np.zeros((h,w,3),dtype=np.uint8)
        x=30+i*4
        if 8 <= i <= 10:
            # temporary occlusion / disappearance
            pass
        else:
            cv2.rectangle(frame,(x,70),(x+60,92),(255,255,255),-1)
        wr.write(frame)
    wr.release()
    item={'start_ms':0,'end_ms':2300,'text':'SHOP','x_percent':18.75,'y_percent':45,'width_percent':18.75,'height_percent':12.3}
    out=_auto_track_ocr_overlay(video,item,interval_ms=200,max_points=12)
    assert out['motion_tracking_enabled']
    assert out['tracking_method'] in {'opencv_template_matching','opencv_template_matching_with_orb_redetection'}
    assert 0 < out['tracking_confidence'] <= 1
    assert all('confidence' in p for p in out['keyframes'])

def test_tracking_does_not_jump_on_unrelated_frame(tmp_path):
    cv2=pytest.importorskip('cv2'); import numpy as np
    video=tmp_path/'unrelated.mp4'; w,h=320,180
    wr=cv2.VideoWriter(str(video),cv2.VideoWriter_fourcc(*'mp4v'),10,(w,h))
    for i in range(12):
        frame=np.zeros((h,w,3),dtype=np.uint8)
        if i<5: cv2.rectangle(frame,(40+i*3,70),(100+i*3,92),(255,255,255),-1)
        else: cv2.rectangle(frame,(230,20),(300,42),(127,127,127),-1)
        wr.write(frame)
    wr.release()
    item={'start_ms':0,'end_ms':1100,'text':'X','x_percent':21.9,'y_percent':45,'width_percent':18.75,'height_percent':12.3}
    out=_auto_track_ocr_overlay(video,item,interval_ms=200,max_points=8)
    xs=[p['x_percent'] for p in out.get('keyframes',[])]
    assert max(xs) < 80
