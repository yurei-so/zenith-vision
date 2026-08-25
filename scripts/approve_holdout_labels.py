from pathlib import Path

from zenith_vision import approve_annotation_batch

dataset = Path.home() / ".local/state/zenith-vision/datasets/operator-holdout-v1"
labels = approve_annotation_batch(dataset, dataset / "annotation-review")
print(f"approved {len(labels)} annotation sets")
