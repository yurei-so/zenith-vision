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
from .capture import (
    CaptureUnavailable, WindowIdentity, WindowSelectionError, XWindowCapture,
    parse_wm_class, select_exact_window,
)

__all__ = [
    "BoundingBox", "DatasetItem", "DatasetManifest", "FusedObservation",
    "CaptureUnavailable", "ManifestError", "MumbleSnapshot", "OcrFailure", "OcrScan", "OcrToken",
    "OcrUnavailable", "RedactionReceipt", "RegionLabel", "RegionMetrics", "RegionProposal",
    "RevealDecision", "TesseractOcr", "TextSafetyDecision", "VisionObservation", "WindowIdentity",
    "WindowSelectionError", "XWindowCapture",
    "assess_text_safety", "evaluate_regions", "fuse_observations", "parse_tesseract_tsv",
    "parse_wm_class", "propose_default_regions", "reverse_reveal", "select_exact_window",
]
