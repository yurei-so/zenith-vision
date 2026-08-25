from pathlib import Path

from zenith_vision import admit_review_batch

state = Path.home() / ".local/state/zenith-vision"
manifest = admit_review_batch(
    state / "review-batches/batch-20260825T005716Z",
    state / "datasets/operator-holdout-v1",
)
print(manifest)
