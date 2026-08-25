from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Iterable


def digest_panel_corpus(directories: Iterable[Path]) -> str:
    """Bind labels and referenced masked tiles without disclosing their content."""
    digest = hashlib.sha256()
    for directory in sorted((path.resolve() for path in directories), key=lambda path: path.name):
        labels_path = directory / "labels.json"
        payload = json.loads(labels_path.read_text(encoding="utf-8"))
        digest.update(directory.name.encode())
        digest.update(b"\0labels\0")
        digest.update(labels_path.read_bytes())
        for item in sorted(payload.get("items", []), key=lambda row: row["id"]):
            for tile in ("left", "center"):
                path = directory / f"{item['id']}-{tile}.png"
                digest.update(path.name.encode())
                digest.update(b"\0")
                digest.update(hashlib.sha256(path.read_bytes()).digest())
    return digest.hexdigest()


def region_plan_digest(plan: list[dict[str, object]]) -> str:
    encoded = json.dumps(plan, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def write_model_bundle(destination: Path, payload: dict[str, object]) -> tuple[Path, str]:
    if payload.get("format") != "zenith-vision.localized-panel-model" or payload.get("version") != 1:
        raise ValueError("unsupported localized panel model bundle")
    encoded = (json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n").encode()
    sha256 = hashlib.sha256(encoded).hexdigest()
    destination.mkdir(parents=True, mode=0o700, exist_ok=True)
    os.chmod(destination, 0o700)
    path = destination / f"panel-localized-{sha256[:16]}.json"
    if path.exists():
        if path.read_bytes() != encoded:
            raise FileExistsError("model bundle digest collision")
        return path, sha256
    temporary = destination / f".{path.name}.{os.getpid()}.tmp"
    try:
        with temporary.open("xb") as handle:
            os.chmod(temporary, 0o600)
            handle.write(encoded)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)
    return path, sha256
