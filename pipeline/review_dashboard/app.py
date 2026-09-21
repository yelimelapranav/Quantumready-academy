"""Internal Streamlit dashboard for previewing generated scripts, quizzes, and
rendered videos before publishing — Pallavi's ClickUp task. Reads directly from
pipeline/output/, no live credentials needed to just browse and approve/reject.

Run: streamlit run pipeline/review_dashboard/app.py
"""
import json
from pathlib import Path

import streamlit as st

OUTPUT_DIR = Path(__file__).parent.parent / "output"
SCRIPTS_DIR = OUTPUT_DIR / "scripts"
QUIZZES_DIR = OUTPUT_DIR / "quizzes"

st.set_page_config(page_title="Quantum Ready Academy — Content Review", layout="wide")
st.title("Lesson content review")

if not SCRIPTS_DIR.exists():
    st.info("No scripts generated yet — run pipeline/scripts_gen/generate_scripts.py first.")
    st.stop()

script_files = sorted(SCRIPTS_DIR.glob("*.txt"))
selected = st.selectbox("Lesson", script_files, format_func=lambda p: p.stem)

if selected:
    st.subheader("Script")
    st.text_area("", selected.read_text(), height=300, label_visibility="collapsed")

    quiz_path = QUIZZES_DIR / (selected.stem + ".json")
    st.subheader("Quiz")
    if quiz_path.exists():
        quiz = json.loads(quiz_path.read_text())
        for q in quiz:
            st.write(f"**{q['question']}**")
            for i, choice in enumerate(q["choices"]):
                marker = "✅" if i == q["answer_index"] else "—"
                st.write(f"{marker} {choice}")
    else:
        st.write("No quiz generated yet for this lesson.")

    # TODO(Pallavi): once video_gen writes into output/raw_video/, add a video preview
    # here (st.video) and an approve/reject button that writes a decision file the
    # batch-render step checks before including a lesson in the final manifest.
