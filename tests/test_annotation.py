from __future__ import annotations

import json
import stat
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from zenith_vision import BoundingBox, create_annotation_proposal


class AnnotationProposalTests(unittest.TestCase):
    def test_creates_private_visible_hud_proposal(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            media = root / "item.png"
            Image.new("RGB", (1280, 720), "navy").save(media)
            overlay, proposal = create_annotation_proposal(media, root / "review", item_id="operator-00001")
            raw = json.loads(proposal.read_text())
            self.assertEqual([item["kind"] for item in raw["labels"]],
                             ["objectives", "skill_bar", "minimap"])
            self.assertEqual(raw["status"], "pending_human_review")
            self.assertEqual(stat.S_IMODE(overlay.stat().st_mode), 0o600)
            self.assertEqual(stat.S_IMODE(proposal.stat().st_mode), 0o600)

    def test_accepts_item_specific_tight_boxes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            media = root / "item.png"
            Image.new("RGB", (100, 100), "navy").save(media)
            boxes = {
                "objectives": BoundingBox(0.8, 0.0, 0.2, 0.3),
                "skill_bar": BoundingBox(0.3, 0.8, 0.4, 0.2),
                "minimap": BoundingBox(0.8, 0.7, 0.2, 0.3),
            }
            _, proposal = create_annotation_proposal(media, root / "review", item_id="item", boxes=boxes)
            raw = json.loads(proposal.read_text())
            self.assertEqual(raw["method"], "item_specific_seed")
            self.assertEqual(raw["labels"][0]["box"], [0.8, 0.0, 0.2, 0.3])


if __name__ == "__main__":
    unittest.main()
