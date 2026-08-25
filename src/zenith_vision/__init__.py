"""Public experiment boundary for Zenith Vision."""

from .fusion import fuse_observations
from .dataset import DatasetItem, DatasetManifest, ManifestError
from .models import BoundingBox, FusedObservation, MumbleSnapshot, VisionObservation
from .layout import RegionLabel, RegionMetrics, RegionProposal, evaluate_regions, propose_default_regions
from .redaction import RedactionReceipt, RevealDecision, reverse_reveal
from .ocr import (
    OcrFailure, OcrScan, OcrToken, OcrUnavailable, TesseractOcr,
    TextSafetyDecision, assess_text_safety, parse_tesseract_tsv,
)

__all__ = [
    "BoundingBox", "DatasetItem", "DatasetManifest", "FusedObservation",
    "ManifestError", "MumbleSnapshot", "OcrFailure", "OcrScan", "OcrToken",
    "OcrUnavailable", "RedactionReceipt", "RegionLabel", "RegionMetrics", "RegionProposal",
    "RevealDecision", "TesseractOcr", "TextSafetyDecision", "VisionObservation",
    "assess_text_safety", "evaluate_regions", "fuse_observations", "parse_tesseract_tsv",
    "propose_default_regions", "reverse_reveal",
]
