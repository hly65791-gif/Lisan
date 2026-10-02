# Lisan OCR Automatic Motion Tracking

Lisan now supports automatic visual tracking for OCR regions.

- OpenCV template matching follows the detected OCR region through sampled frames.
- Tracking is generated automatically during the OCR stage when `LISAN_OCR_AUTO_TRACK=true`.
- Default sample interval: 500 ms.
- Default maximum points per overlay: 24.
- Low-confidence matches are skipped rather than jumping to unrelated content.
- The result is stored in `ocr.json` as `keyframes` and consumed by subtitle rendering and original-text replacement.
- `tracking_method=opencv_template_matching` identifies the algorithm used.

This is visual template tracking, not semantic object tracking or AI inpainting. Complex occlusion, cuts, rotations, and major appearance changes may require manual keyframes.
