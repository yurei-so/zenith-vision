from __future__ import annotations

import json
import os
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageDraw


def difference_hash(image: Image.Image) -> int:
    pixels = list(image.convert("L").resize((9, 8), Image.Resampling.LANCZOS).getdata())
    value = 0
    for row in range(8):
        for column in range(8):
            value = (value << 1) | int(pixels[row * 9 + column] > pixels[row * 9 + column + 1])
    return value


def hamming_distance(left: int, right: int) -> int:
    return (left ^ right).bit_count()


def is_distinct(candidate: int, accepted: list[int], *, minimum_distance: int = 8) -> bool:
    if not 0 <= minimum_distance <= 64:
        raise ValueError("minimum_distance must be between 0 and 64")
    return all(hamming_distance(candidate, previous) >= minimum_distance for previous in accepted)


def save_batch_manifest(directory: Path, entries: list[dict[str, object]], *, started_at: str) -> Path:
    path = directory / "batch.json"
    payload = {
        "format": "zenith-vision.review-batch", "version": 1,
        "started_at": started_at, "completed_at": datetime.now(timezone.utc).isoformat(),
        "status": "pending_human_review", "candidate_count": len(entries), "candidates": entries,
    }
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    os.chmod(temporary, 0o600)
    os.replace(temporary, path)
    return path


def create_contact_sheet(images: list[tuple[str, Path]], destination: Path) -> Path:
    if not images:
        raise ValueError("contact sheet requires at least one image")
    thumb_width, thumb_height = 480, 270
    columns = 2
    rows = (len(images) + columns - 1) // columns
    sheet = Image.new("RGB", (columns * thumb_width, rows * (thumb_height + 28)), "#16161b")
    draw = ImageDraw.Draw(sheet)
    for index, (label, path) in enumerate(images):
        with Image.open(path) as source:
            thumb = source.convert("RGB")
            thumb.thumbnail((thumb_width, thumb_height), Image.Resampling.LANCZOS)
        x = (index % columns) * thumb_width
        y = (index // columns) * (thumb_height + 28)
        sheet.paste(thumb, (x, y))
        draw.text((x + 8, y + thumb_height + 6), label, fill="#ffffff")
    temporary = destination.with_name(f".{destination.name}.tmp")
    sheet.save(temporary, format="PNG", optimize=True)
    os.chmod(temporary, 0o600)
    os.replace(temporary, destination)
    return destination
