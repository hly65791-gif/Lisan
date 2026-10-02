# Lisan v0.33 — OCR Motion Tracking

## What changed
- OCR overlays can now enable `motion_tracking_enabled`.
- Each tracked overlay stores time-based keyframes containing x/y position and box size.
- The editor can add a keyframe at the current video position and dragging a tracked OCR overlay records/updates the keyframe at the current playhead.
- Backend validation limits keyframes to the OCR time range and a maximum of 120 points per overlay.
- ASS output is split into time segments so translated OCR text follows the tracked keyframe positions.
- Original-text replacement (`delogo`) is split into the same segments, keeping the removal region synchronized with the tracked text.

## Important limitation
This version implements deterministic keyframe-based motion tracking. It does not claim automatic visual object tracking from pixels. Automatic computer-vision tracking can be added later as a separate provider without changing the saved keyframe contract.

## Verification
- Python compile: PASS
- Backend tests: 44/44 PASS
