import argparse
import json
from pathlib import Path

from PIL import Image

from zenith_vision import BoundingBox, DatasetManifest, RegionLabel, evaluate_regions, propose_default_regions

parser = argparse.ArgumentParser()
parser.add_argument("dataset_name")
args = parser.parse_args()
dataset = Path.home() / ".local/state/zenith-vision/datasets" / args.dataset_name
manifest = DatasetManifest.load(dataset / "manifest.json")
matched = expected = proposed = 0
weighted_iou = 0.0
for item in manifest.items:
    if item.labels_path is None:
        raise RuntimeError(f"{item.item_id}: labels are not approved")
    raw = json.loads(Path(item.labels_path).read_text(encoding="utf-8"))
    labels = tuple(RegionLabel(row["kind"], BoundingBox(*row["box"])) for row in raw["regions"])
    with Image.open(item.media_path) as image:
        metrics = evaluate_regions(propose_default_regions(*image.size), labels)
    matched += metrics.matched
    expected += metrics.expected
    proposed += metrics.proposed
    weighted_iou += metrics.mean_iou * metrics.expected
result = {
    "format": "zenith-vision.holdout-result", "version": 1,
    "dataset": manifest.name, "items": len(manifest.items),
    "labels": expected, "matched": matched, "proposals_evaluated": proposed,
    "mean_iou": round(weighted_iou / expected, 6),
    "recall_at_50": round(matched / expected, 6),
}
print(json.dumps(result, separators=(",", ":")))
