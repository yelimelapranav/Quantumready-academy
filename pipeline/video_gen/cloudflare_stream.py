"""Upload a rendered lesson video to Cloudflare Stream. Written against Cloudflare's
documented direct-upload API — verify against https://developers.cloudflare.com/stream
before relying on it in production.
"""
from pathlib import Path

import requests

from pipeline.config import config


def upload(video_path: Path) -> str:
    """Upload a local video file to Cloudflare Stream, return its Stream video id
    (this is the value that goes in lessons.cloudflare_video_id / the manifest).
    """
    url = f"https://api.cloudflare.com/client/v4/accounts/{config.cloudflare_account_id}/stream"

    with open(video_path, "rb") as f:
        resp = requests.post(
            url,
            headers={"Authorization": f"Bearer {config.cloudflare_stream_api_token}"},
            files={"file": f},
        )
    resp.raise_for_status()
    return resp.json()["result"]["uid"]
