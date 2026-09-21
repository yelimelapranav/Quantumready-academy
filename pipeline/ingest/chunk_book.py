"""Step 1: turn the book into structured, chunked JSON ready for script generation.

TODO(Pallavi): wire the real extraction for whatever format the book source is in
(PDF via PyPDF2, or .docx via python-docx). The chunking boundary is currently "one
chapter = one chunk" — revisit if chapters are long enough that the LLM step in
generate_scripts.py needs sub-chapter chunks instead.

Usage: python -m pipeline.ingest.chunk_book --input path/to/book.pdf
"""
import argparse
import json
from pathlib import Path

OUTPUT_PATH = Path(__file__).parent.parent / "output" / "chunks.json"


def extract_chapters(input_path: Path) -> list[dict]:
    """Return a list of {"chapter": str, "text": str} in book order.

    TODO(Pallavi): replace this stub with real extraction. Chapter boundaries will
    likely need a heuristic (heading detection, a manually-maintained table of
    contents with page ranges, or manual splitting) rather than something fully
    automatic — the book's actual structure should decide which.
    """
    raise NotImplementedError("Implement chapter extraction for the book's source format")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    args = parser.parse_args()

    chapters = extract_chapters(args.input)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(chapters, indent=2))
    print(f"Wrote {len(chapters)} chapter chunks to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
