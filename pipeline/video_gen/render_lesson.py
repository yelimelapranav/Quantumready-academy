"""Orchestrates the full per-lesson video step: reviewed script -> HeyGen render ->
download -> Cloudflare Stream upload -> a manifest-ready dict.

This is what the "[Shared] Batch-render all lessons" ClickUp task loops over every
approved script to build pipeline/output/manifest.json.

Usage: python -m pipeline.video_gen.render_lesson --script pipeline/output/scripts/lesson-00.txt --slug lesson-00-welcome --order 0 --title "Welcome"
"""
import argparse
import json
from pathlib import Path

from pipeline.video_gen import cloudflare_stream, heygen_client

RAW_VIDEO_DIR = Path(__file__).parent.parent / "output" / "raw_video"


def render_lesson(script_path: Path, slug: str, order_index: int, title: str) -> dict:
    script_text = script_path.read_text()

    video_id = heygen_client.submit_render(script_text)
    video_url = heygen_client.poll_until_ready(video_id)
    local_path = heygen_client.download(video_url, RAW_VIDEO_DIR / f"{slug}.mp4")

    cloudflare_video_id = cloudflare_stream.upload(local_path)

    # Quiz is attached separately by the batch-render step, which reads
    # pipeline/output/quizzes/<same-stem>.json — this function only owns video.
    return {
        "slug": slug,
        "order_index": order_index,
        "title": title,
        "transcript": script_text,
        "cloudflare_video_id": cloudflare_video_id,
        "duration_seconds": None,  # TODO(Pallavi): pull real duration from HeyGen's response or ffprobe
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--script", required=True, type=Path)
    parser.add_argument("--slug", required=True)
    parser.add_argument("--order", required=True, type=int)
    parser.add_argument("--title", required=True)
    args = parser.parse_args()

    result = render_lesson(args.script, args.slug, args.order, args.title)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
