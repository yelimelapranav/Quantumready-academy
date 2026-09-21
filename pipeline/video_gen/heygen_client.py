"""Thin wrapper around the HeyGen video-generation API: submit a script, poll until
the render finishes, download the result. Real endpoint shapes may drift — check
https://docs.heygen.com against this before relying on it; written from the documented
v2 video-generation flow, not yet tested against a live key.
"""
import time
from pathlib import Path

import requests

from pipeline.config import config

API_BASE = "https://api.heygen.com/v2"


def submit_render(script_text: str) -> str:
    """Kick off a render, return HeyGen's video_id."""
    resp = requests.post(
        f"{API_BASE}/video/generate",
        headers={"X-Api-Key": config.heygen_api_key},
        json={
            "video_inputs": [
                {
                    "character": {"type": "avatar", "avatar_id": config.heygen_avatar_id},
                    "voice": {"type": "text", "input_text": script_text, "voice_id": config.heygen_voice_id},
                }
            ],
            "dimension": {"width": 1920, "height": 1080},
        },
    )
    resp.raise_for_status()
    return resp.json()["data"]["video_id"]


def poll_until_ready(video_id: str, timeout_seconds: int = 900, interval_seconds: int = 15) -> str:
    """Poll HeyGen's status endpoint until the render completes, return the video URL.

    TODO(Pallavi): swap polling for a webhook once batch volume makes polling every
    lesson expensive — HeyGen supports callback URLs on the generate call.
    """
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        resp = requests.get(
            f"{API_BASE}/video_status.get",
            headers={"X-Api-Key": config.heygen_api_key},
            params={"video_id": video_id},
        )
        resp.raise_for_status()
        status = resp.json()["data"]["status"]

        if status == "completed":
            return resp.json()["data"]["video_url"]
        if status == "failed":
            raise RuntimeError(f"HeyGen render failed for video_id={video_id}")

        time.sleep(interval_seconds)

    raise TimeoutError(f"HeyGen render for video_id={video_id} did not finish within {timeout_seconds}s")


def download(video_url: str, out_path: Path) -> Path:
    resp = requests.get(video_url, stream=True)
    resp.raise_for_status()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)
    return out_path
