import html
import os

import streamlit as st

from database.database import get_all_lectures, get_notes
from models.keyword_extractor import extract_keywords_scored
from services.export_docx import export_notes_to_docx
from services.export_pdf import export_notes_to_pdf
from utils.styles import inject_css, keyword_pills_html, page_header

inject_css()
page_header("Notes Viewer", "Review generated summaries, concepts, and export-ready study notes.")

GENERATED_DIR = os.path.join(os.path.dirname(__file__), "..", "generated")
os.makedirs(GENERATED_DIR, exist_ok=True)

lectures = get_all_lectures()
if not lectures:
    st.warning("No lectures found. Please upload a lecture first.")
    st.stop()

options = {lec["id"]: lec["title"] for lec in lectures}
selected_id = st.selectbox("Select a lecture", options=list(options.keys()), format_func=lambda x: options[x])
lec_title = options[selected_id]
notes = get_notes(selected_id)

if not notes:
    st.info("No notes generated yet. Please go to Notes Generator first.")
    st.stop()

st.markdown("### Executive Summary")
summary = notes.get("summary", "")
if summary:
    lines = [line.strip() for line in summary.split("\n") if line.strip()]
    formatted_lines = []
    for line in lines:
        if line.startswith("•"):
            formatted_lines.append(f"- {line[1:].strip()}")
        else:
            formatted_lines.append(line)
    st.markdown("\n".join(formatted_lines))
else:
    st.info("Summary not available.")

st.markdown("---")
st.markdown("### Key Concepts")

raw_keywords = notes.get("keywords", "")
kw_list = [k.strip() for k in raw_keywords.split(",") if k.strip()]

if kw_list:
    text_path = os.path.join(os.path.dirname(__file__), "..", "uploads", "texts", f"{selected_id}.txt")
    scored = []
    if os.path.exists(text_path):
        try:
            with open(text_path, "r", encoding="utf-8") as f:
                raw_text = f.read()
            scored = extract_keywords_scored(raw_text, top_n=len(kw_list))
        except Exception:
            pass

    if scored:
        score_map = {kw: score for kw, score in scored}
        max_s = max(score_map.values()) if score_map else 1
        pills_html = "<div style='margin: 0.5rem 0 1rem 0;'>"
        for kw in kw_list:
            score = score_map.get(kw, 0.3)
            opacity = 0.55 + 0.45 * (score / max_s)
            pills_html += (
                f"<span class='kw-pill' style='opacity:{opacity:.2f};' "
                f"title='Relevance: {score:.0%}'>{html.escape(kw)}</span>"
            )
        pills_html += "</div>"
    else:
        pills_html = keyword_pills_html(kw_list)
    st.html(pills_html)
else:
    st.info("No keywords extracted.")

st.markdown("---")
st.markdown("### Export Notes")
ec1, ec2, ec3 = st.columns(3)

with ec1:
    if st.button("Export as PDF", use_container_width=True):
        with st.spinner("Generating PDF..."):
            try:
                path = export_notes_to_pdf(lec_title, summary, kw_list, GENERATED_DIR)
                with open(path, "rb") as f:
                    st.download_button(
                        "Download PDF",
                        data=f.read(),
                        file_name=os.path.basename(path),
                        mime="application/pdf",
                        use_container_width=True,
                    )
            except Exception as exc:
                st.error(f"PDF export failed: {exc}")

with ec2:
    if st.button("Export as DOCX", use_container_width=True):
        with st.spinner("Generating DOCX..."):
            try:
                path = export_notes_to_docx(lec_title, summary, kw_list, GENERATED_DIR)
                with open(path, "rb") as f:
                    st.download_button(
                        "Download DOCX",
                        data=f.read(),
                        file_name=os.path.basename(path),
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        use_container_width=True,
                    )
            except Exception as exc:
                st.error(f"DOCX export failed: {exc}")

with ec3:
    if st.button("Show Copyable Summary", use_container_width=True):
        st.code(summary, language=None)
        st.caption("Select the text above to copy it.")

if notes.get("generated_at"):
    st.html(
        f"<small>Notes last generated: {html.escape(notes['generated_at'][:16].replace('T', ' '))}</small>"
    )
