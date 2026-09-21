"""Sanity-checks pipeline/output/manifest.json before it's handed to the platform lane.
Run this as the last step of the batch-render task — a manifest that fails these checks
should never be handed off.

Usage: python -m pipeline.manifest.validate_manifest
"""
import json
import sys
from pathlib import Path

from pipeline.manifest.schema import Manifest

MANIFEST_PATH = Path(__file__).parent.parent / "output" / "manifest.json"


def validate() -> None:
    if not MANIFEST_PATH.exists():
        sys.exit(f"No manifest found at {MANIFEST_PATH} — run the batch-render step first.")

    raw = json.loads(MANIFEST_PATH.read_text())
    manifest = Manifest(lessons=raw)  # raises pydantic.ValidationError on shape mismatches

    slugs = [l.slug for l in manifest.lessons]
    if len(slugs) != len(set(slugs)):
        sys.exit("Duplicate slugs in manifest — every lesson needs a unique slug.")

    orders = [l.order_index for l in manifest.lessons]
    if len(orders) != len(set(orders)):
        sys.exit("Duplicate order_index values in manifest.")

    missing_video = [l.slug for l in manifest.lessons if not l.cloudflare_video_id]
    if missing_video:
        print(f"WARNING: {len(missing_video)} lesson(s) have no cloudflare_video_id yet: {missing_video}")

    print(f"OK — {len(manifest.lessons)} lessons validated.")


if __name__ == "__main__":
    validate()
