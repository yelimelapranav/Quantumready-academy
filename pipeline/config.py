"""Central env/config loading for the content pipeline. Every module below imports
from here rather than calling os.environ directly, so there's one place to see what
the pipeline needs and one place to fail loudly if something's missing.
"""
import os
from dotenv import load_dotenv

load_dotenv()


def require(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Missing required env var: {name} (see pipeline/.env.example)")
    return value


class Config:
    # Loaded lazily via properties so `import config` doesn't crash before .env exists —
    # only blows up when a module actually tries to use a given credential.
    @property
    def anthropic_api_key(self) -> str:
        return require("ANTHROPIC_API_KEY")

    @property
    def heygen_api_key(self) -> str:
        return require("HEYGEN_API_KEY")

    @property
    def heygen_avatar_id(self) -> str:
        return require("HEYGEN_AVATAR_ID")

    @property
    def heygen_voice_id(self) -> str:
        return require("HEYGEN_VOICE_ID")

    @property
    def cloudflare_account_id(self) -> str:
        return require("CLOUDFLARE_ACCOUNT_ID")

    @property
    def cloudflare_stream_api_token(self) -> str:
        return require("CLOUDFLARE_STREAM_API_TOKEN")


config = Config()
