"""Public experiment boundary for Zenith Vision."""

from .fusion import fuse_observations
from .dataset import DatasetItem, DatasetManifest, ManifestError
from .models import BoundingBox, FusedObservation, MumbleSnapshot, VisionObservation
from .layout import RegionLabel, RegionMetrics, RegionProposal, evaluate_regions, propose_default_regions
from .redaction import RedactionReceipt, RevealDecision, mask_regions, reverse_reveal
from .ocr import (
    OcrFailure, OcrScan, OcrToken, OcrUnavailable, TesseractOcr,
    TextSafetyDecision, assess_text_safety, mask_ocr_tokens, parse_tesseract_tsv,
)
from .capture import (
    CaptureUnavailable, WindowIdentity, WindowSelectionError, XWindowCapture,
    parse_wm_class, select_exact_window,
)
from .synthetic import generate_synthetic_corpus
from .review import ReviewCandidateReceipt, save_review_candidate
from .admission import admit_review_batch, admit_review_candidate
from .annotation import (
    VISIBLE_HUD_LABELS, approve_annotation_batch, approve_annotation_proposal,
    create_annotation_proposal,
)
from .collection import create_contact_sheet, difference_hash, hamming_distance, is_distinct, save_batch_manifest

__all__ = [
    "BoundingBox", "DatasetItem", "DatasetManifest", "FusedObservation",
    "CaptureUnavailable", "ManifestError", "MumbleSnapshot", "OcrFailure", "OcrScan", "OcrToken",
    "OcrUnavailable", "RedactionReceipt", "RegionLabel", "RegionMetrics", "RegionProposal",
    "ReviewCandidateReceipt",
    "RevealDecision", "TesseractOcr", "TextSafetyDecision", "VISIBLE_HUD_LABELS",
    "VisionObservation", "WindowIdentity",
    "WindowSelectionError", "XWindowCapture",
    "admit_review_batch", "admit_review_candidate", "approve_annotation_batch",
    "approve_annotation_proposal", "assess_text_safety",
    "create_annotation_proposal", "create_contact_sheet", "difference_hash", "evaluate_regions",
    "fuse_observations", "generate_synthetic_corpus",
    "hamming_distance", "is_distinct", "mask_ocr_tokens", "mask_regions",
    "parse_tesseract_tsv",
    "parse_wm_class", "propose_default_regions", "reverse_reveal", "save_review_candidate",
    "save_batch_manifest", "select_exact_window",
]
