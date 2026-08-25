from __future__ import annotations

import json

from zenith_vision import TesseractOcr, XWindowCapture, assess_text_safety, reverse_reveal, select_exact_window

capture = XWindowCapture()
target = select_exact_window(
    capture.list_windows(), title="Guild Wars 2",
    instance="steam_app_1284210", window_class="steam_app_1284210",
)
frame = capture.capture(target)
scan = TesseractOcr().scan(frame)
text_gate = assess_text_safety(scan)
sanitized, receipt = reverse_reveal(frame, [])
assert sanitized.getbbox() is None
assert receipt.revealed_pixels == 0
print(json.dumps({
    "format": "zenith-vision.local-capture-smoke", "version": 1, "status": "ok",
    "target": {"title": target.title, "instance": target.instance, "window_class": target.window_class},
    "frame": {"width": frame.width, "height": frame.height},
    "ocr": {"complete": scan.complete, "token_count": len(scan.tokens),
            "default_reveal_allowed": text_gate.safe_to_reveal},
    "redaction": {"revealed_pixels": receipt.revealed_pixels,
                  "revealed_fraction": receipt.revealed_fraction},
}, separators=(",", ":")))
