"""Step 3: reviewed lesson script -> quiz questions, via LLM.

Mirrors the "generate structured, scored output from source content" pattern already
used in the team's Mock Interview Coach project — same shape, different content.

Usage: python -m pipeline.quiz_gen.generate_quiz --script pipeline/output/scripts/lesson-00.txt
"""
import argparse
import json
from pathlib import Path

import anthropic

from pipeline.config import config
from pipeline.manifest.schema import QuizQuestion

QUIZ_PROMPT = """Generate 2-3 multiple-choice quiz questions testing the single most
important idea from this lesson script. Each question needs exactly 4 choices and one
correct answer_index (0-based). Return ONLY valid JSON matching this shape:

[{{"question": "...", "choices": ["...", "...", "...", "..."], "answer_index": 0}}]

Lesson script:
{script_text}
"""


def generate_quiz(client: anthropic.Anthropic, script_text: str) -> list[QuizQuestion]:
    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": QUIZ_PROMPT.format(script_text=script_text)}],
    )
    # TODO(Pallavi): add retry/repair logic for malformed JSON — LLM output isn't
    # guaranteed valid JSON on the first try, and this is a batch job.
    raw = json.loads(message.content[0].text)
    return [QuizQuestion(**q) for q in raw]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--script", required=True, type=Path)
    args = parser.parse_args()

    client = anthropic.Anthropic(api_key=config.anthropic_api_key)
    quiz = generate_quiz(client, args.script.read_text())

    out_path = args.script.parent.parent / "quizzes" / (args.script.stem + ".json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps([q.model_dump() for q in quiz], indent=2))
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
