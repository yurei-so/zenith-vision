"""Public experiment boundary for Zenith Vision."""

from .fusion import fuse_observations
from .dataset import DatasetItem, DatasetManifest, ManifestError
from .models import BoundingBox, FusedObservation, MumbleSnapshot, VisionObservation
from .layout import RegionLabel, RegionMetrics, RegionProposal, evaluate_regions, propose_default_regions
from .redaction import RedactionReceipt, RevealDecision, reverse_reveal

__all__ = [
    "BoundingBox", "DatasetItem", "DatasetManifest", "FusedObservation",
    "ManifestError", "MumbleSnapshot", "RedactionReceipt", "RegionLabel", "RegionMetrics",
    "RegionProposal", "RevealDecision", "VisionObservation", "evaluate_regions",
    "fuse_observations", "propose_default_regions", "reverse_reveal",
]
