"""Step 2: chapter chunk -> lesson script, via LLM.

Reads pipeline/output/chunks.json (from ingest/chunk_book.py), writes one script per
chapter to pipeline/output/scripts/. Human review checkpoint: nothing past this step
should run automatically — someone reads and approves each script before quiz
generation or video rendering touches it.

Usage: python -m pipeline.scripts_gen.generate_scripts
"""
import json
from pathlib import Path

import anthropic

from pipeline.config import config

CHUNKS_PATH = Path(__file__).parent.parent / "output" / "chunks.json"
SCRIPTS_DIR = Path(__file__).parent.parent / "output" / "scripts"
PROMPT_TEMPLATE = (Path(__file__).parent / "prompts" / "lesson_script_prompt.txt").read_text()


def generate_script(client: anthropic.Anthropic, chapter_title: str, chapter_text: str) -> str:
    prompt = PROMPT_TEMPLATE.format(chapter_title=chapter_title, chapter_text=chapter_text)

    # TODO(Pallavi): pick the right model for this workspace's Anthropic account/tier,
    # and consider whether chapter_text needs truncation/summarization first for very
    # long chapters (context window headroom).
    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


def main() -> None:
    chapters = json.loads(CHUNKS_PATH.read_text())
    client = anthropic.Anthropic(api_key=config.anthropic_api_key)

    SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)

    for i, chapter in enumerate(chapters):
        script = generate_script(client, chapter["chapter"], chapter["text"])
        out_path = SCRIPTS_DIR / f"lesson-{i:02d}.txt"
        out_path.write_text(script)
        print(f"Wrote {out_path}")

    print(f"\n{len(chapters)} scripts generated — review each before running quiz_gen or video_gen.")


if __name__ == "__main__":
    main()
