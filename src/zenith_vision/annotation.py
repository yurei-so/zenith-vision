from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageDraw

from .layout import DEFAULT_REGION_BOXES
from .models import BoundingBox


VISIBLE_HUD_LABELS = ("objectives", "skill_bar", "minimap")


def create_annotation_proposal(
    media: Path,
    output_directory: Path,
    *,
    item_id: str,
    boxes: dict[str, BoundingBox] | None = None,
    now: datetime | None = None,
) -> tuple[Path, Path]:
    """Create a private geometry-seeded label proposal and visual overlay."""
    media = media.resolve()
    output_directory = output_directory.resolve()
    output_directory.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(output_directory, 0o700)
    digest = hashlib.sha256(media.read_bytes()).hexdigest()
    with Image.open(media) as source:
        overlay = source.convert("RGB").copy()
    draw = ImageDraw.Draw(overlay)
    labels: list[dict[str, object]] = []
    colors = {"objectives": "#ffcc33", "skill_bar": "#39e67a", "minimap": "#4db5ff"}
    selected_boxes = boxes or {kind: DEFAULT_REGION_BOXES[kind] for kind in VISIBLE_HUD_LABELS}
    if set(selected_boxes) != set(VISIBLE_HUD_LABELS):
        raise ValueError("annotation proposal requires exactly the visible HUD labels")
    for kind in VISIBLE_HUD_LABELS:
        box = selected_boxes[kind]
        pixels = (round(box.x * overlay.width), round(box.y * overlay.height),
                  round((box.x + box.width) * overlay.width),
                  round((box.y + box.height) * overlay.height))
        draw.rectangle(pixels, outline=colors[kind], width=max(3, overlay.width // 400))
        draw.rectangle((pixels[0], pixels[1], pixels[0] + 12 + len(kind) * 10, pixels[1] + 24), fill="#000000")
        draw.text((pixels[0] + 5, pixels[1] + 4), kind, fill=colors[kind])
        labels.append({"kind": kind, "box": [box.x, box.y, box.width, box.height]})
    current = now or datetime.now(timezone.utc)
    proposal = {
        "format": "zenith-vision.annotation-proposal", "version": 1,
        "item_id": item_id, "media_sha256": digest,
        "created_at": current.isoformat(),
        "method": "item_specific_seed" if boxes is not None else "gw2_default_layout_baseline",
        "status": "pending_human_review", "labels": labels,
    }
    overlay_path = output_directory / f"{item_id}-overlay.png"
    proposal_path = output_directory / f"{item_id}-proposal.json"
    overlay.save(overlay_path, format="PNG", optimize=True)
    proposal_path.write_text(json.dumps(proposal, indent=2) + "\n", encoding="utf-8")
    os.chmod(overlay_path, 0o600)
    os.chmod(proposal_path, 0o600)
    return overlay_path, proposal_path
