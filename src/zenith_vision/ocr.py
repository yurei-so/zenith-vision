from __future__ import annotations

import csv
import io
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from PIL import Image


class OcrUnavailable(RuntimeError):
    pass


class OcrFailure(RuntimeError):
    pass


@dataclass(frozen=True)
class OcrToken:
    text: str
    confidence: float


@dataclass(frozen=True)
class OcrScan:
    tokens: tuple[OcrToken, ...]
    backend: str
    complete: bool


@dataclass(frozen=True)
class TextSafetyDecision:
    safe_to_reveal: bool
    reason: str
    token_count: int


class TesseractOcr:
    """Bounded local OCR. Source pixels are written only to an owner-only temp file."""

    def __init__(self, executable: str = "tesseract", timeout_seconds: float = 10.0) -> None:
        resolved = shutil.which(executable)
        if resolved is None:
            raise OcrUnavailable("tesseract executable is not installed")
        self.executable = resolved
        self.timeout_seconds = timeout_seconds

    def scan(self, image: Image.Image) -> OcrScan:
        with tempfile.TemporaryDirectory(prefix="zenith-vision-ocr-") as directory:
            path = Path(directory) / "region.png"
            image.convert("RGB").save(path, format="PNG")
            try:
                result = subprocess.run(
                    [self.executable, str(path), "stdout", "--psm", "6", "tsv"],
                    stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    check=False, timeout=self.timeout_seconds, text=True,
                )
            except subprocess.TimeoutExpired as error:
                raise OcrFailure("tesseract timed out") from error
            if result.returncode != 0:
                raise OcrFailure(f"tesseract exited with status {result.returncode}")
            return parse_tesseract_tsv(result.stdout)


def parse_tesseract_tsv(value: str) -> OcrScan:
    try:
        rows = csv.DictReader(io.StringIO(value), delimiter="\t")
        if rows.fieldnames is None or not {"text", "conf"}.issubset(rows.fieldnames):
            raise ValueError("missing TSV columns")
        tokens: list[OcrToken] = []
        for row in rows:
            text = (row.get("text") or "").strip()
            if not text:
                continue
            confidence = float(row.get("conf") or "-1") / 100.0
            tokens.append(OcrToken(text=text, confidence=max(0.0, min(1.0, confidence))))
        return OcrScan(tokens=tuple(tokens), backend="tesseract", complete=True)
    except (csv.Error, TypeError, ValueError) as error:
        raise OcrFailure("invalid tesseract TSV output") from error


def assess_text_safety(
    scan: OcrScan,
    *,
    allowed_text: Iterable[str] = (),
    minimum_confidence: float = 0.85,
) -> TextSafetyDecision:
    """Fail closed unless OCR completed and every token is confidently allowlisted."""
    if not scan.complete:
        return TextSafetyDecision(False, "ocr_incomplete", len(scan.tokens))
    allowed = {_normalize(item) for item in allowed_text if _normalize(item)}
    for token in scan.tokens:
        if token.confidence < minimum_confidence:
            return TextSafetyDecision(False, "ambiguous_text", len(scan.tokens))
        if _normalize(token.text) not in allowed:
            return TextSafetyDecision(False, "unapproved_text", len(scan.tokens))
    return TextSafetyDecision(True, "ocr_clean", len(scan.tokens))


def _normalize(value: str) -> str:
    return " ".join(value.casefold().split())
