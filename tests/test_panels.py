from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from zenith_vision.ocr import OcrScan, OcrToken
from zenith_vision.panels import recognize_panel_titles, scan_panel_titles
from PIL import Image


class RecordingOcr:
    def __init__(self, scan: OcrScan) -> None:
        self.result = scan
        self.size = None

    def scan(self, image: Image.Image) -> OcrScan:
        self.size = image.size
        return self.result


class PanelRecognitionTests(unittest.TestCase):
    def test_recognizes_multiple_allowlisted_panels_only(self) -> None:
        scan = OcrScan((
            OcrToken("Inventory", 0.96), OcrToken("private-item-name", 0.99),
            OcrToken("Hero", 0.91),
        ), "fake", True)
        result = recognize_panel_titles(scan)
        self.assertEqual(result.panels, ("hero", "inventory"))
        self.assertEqual(result.status, "recognized")
        self.assertEqual(result.confidence, 0.91)

    def test_reports_none_without_disclosing_other_text(self) -> None:
        result = recognize_panel_titles(OcrScan((OcrToken("Kasube!", 0.99),), "fake", True))
        self.assertEqual(result.panels, ())
        self.assertEqual(result.status, "none")

    def test_low_confidence_title_abstains(self) -> None:
        result = recognize_panel_titles(OcrScan((OcrToken("Inventory", 0.70),), "fake", True))
        self.assertEqual(result.status, "uncertain")

    def test_incomplete_scan_abstains(self) -> None:
        result = recognize_panel_titles(OcrScan((), "fake", False))
        self.assertEqual(result.status, "uncertain")

    def test_scans_enlarged_central_search_area(self) -> None:
        backend = RecordingOcr(OcrScan((OcrToken("Hero", 0.95),), "fake", True))
        result = scan_panel_titles(Image.new("RGB", (1000, 500)), backend)
        self.assertEqual(result.panels, ("hero",))
        self.assertEqual(backend.size, (1300, 700))

    def test_rejects_tiny_frame(self) -> None:
        backend = RecordingOcr(OcrScan((), "fake", True))
        with self.assertRaisesRegex(ValueError, "640x480"):
            scan_panel_titles(Image.new("RGB", (320, 240)), backend)


if __name__ == "__main__":
    unittest.main()
