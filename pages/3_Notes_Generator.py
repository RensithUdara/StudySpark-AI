import html
import os

import streamlit as st

from database.database import get_all_lectures, get_notes, save_notes
from models.keyword_extractor import extract_keywords
from models.rag_engine import build_faiss_index
from models.summarizer import generate_summary
from utils.styles import inject_css, page_header

inject_css()
page_header("Notes Generator", "Create summaries, keywords, and the searchable knowledge base.")

lectures = get_all_lectures()
if not lectures:
    st.warning("No lectures found. Please upload a lecture first.")
    st.stop()

options = {lec["id"]: lec["title"] for lec in lectures}
selected_id = st.selectbox("Select a lecture", options=list(options.keys()), format_func=lambda x: options[x])

existing_notes = get_notes(selected_id)

if existing_notes:
    st.html(
        """
        <div class="info-strip">
            <strong>Notes already exist.</strong>
            Regenerate them to refresh the summary, keywords, and search index.
        </div>
        """
    )
    btn_label = "Regenerate Notes and Index"
else:
    btn_label = "Generate Notes and Index"

if st.button(btn_label):
    text_path = os.path.join(os.path.dirname(__file__), "..", "uploads", "texts", f"{selected_id}.txt")
    if not os.path.exists(text_path):
        st.error("Source text not found. Please re-upload the lecture.")
        st.stop()

    with open(text_path, "r", encoding="utf-8") as f:
        text = f.read()

    progress = st.progress(0)
    steps = [
        ("Generating structured summary with AI...", 15),
        ("Extracting key concepts and keywords...", 50),
        ("Building the searchable knowledge base...", 80),
        ("Saving study materials to the database...", 95),
    ]
    step_placeholders = [st.empty() for _ in steps]

    def render_steps(active_idx: int):
        for i, (msg, _) in enumerate(steps):
            safe_msg = html.escape(msg)
            if i < active_idx:
                step_placeholders[i].html(f"<div class='step-item done'>{safe_msg}</div>")
            elif i == active_idx:
                step_placeholders[i].html(f"<div class='step-item active'>{safe_msg}</div>")
            else:
                step_placeholders[i].html(f"<div class='step-item'>{safe_msg}</div>")

    try:
        render_steps(0)
        progress.progress(15)
        with st.spinner("AI is reading the lecture and synthesizing a summary..."):
            summary = generate_summary(text)

        render_steps(1)
        progress.progress(50)
        with st.spinner("Extracting important concepts..."):
            keywords = extract_keywords(text)

        render_steps(2)
        progress.progress(80)
        with st.spinner("Building vector search for the study assistant..."):
            build_faiss_index(selected_id, text)

        render_steps(3)
        progress.progress(95)
        save_notes(selected_id, summary, keywords)

        progress.progress(100)
        render_steps(len(steps))
        st.success("Notes generated successfully. Open Notes Viewer or AI Study Assistant to continue.")

    except Exception as exc:
        st.error(f"Error during generation: {exc}")
