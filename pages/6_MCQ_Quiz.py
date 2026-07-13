import html
import os

import plotly.graph_objects as go
import streamlit as st

from database.database import get_all_lectures, get_mcqs, save_mcqs, save_quiz_result
from models.mcq_generator import generate_mcqs
from utils.styles import inject_css, page_header, score_badge_html

inject_css()
page_header("MCQ Quiz", "Test your understanding with AI-generated multiple-choice questions.")

lectures = get_all_lectures()
if not lectures:
    st.warning("No lectures found. Please upload a lecture first.")
    st.stop()

options = {lec["id"]: lec["title"] for lec in lectures}
selected_id = st.selectbox("Select lecture for quiz", options=list(options.keys()), format_func=lambda x: options[x])

mcqs = get_mcqs(selected_id)

if not mcqs:
    st.info("No MCQs found for this lecture.")
    num_q = st.slider("How many questions to generate?", 3, 15, 8)
    if st.button("Generate MCQs"):
        text_path = os.path.join(os.path.dirname(__file__), "..", "uploads", "texts", f"{selected_id}.txt")
        if os.path.exists(text_path):
            with st.spinner("Generating questions using AI..."):
                with open(text_path, "r", encoding="utf-8") as f:
                    text = f.read()
                new_mcqs = generate_mcqs(text, num_mcqs=num_q)
                save_mcqs(selected_id, new_mcqs)
            st.success(f"{len(new_mcqs)} MCQs generated.")
            st.rerun()
        else:
            st.error("Source text not found. Please re-upload the lecture.")
    st.stop()

st.markdown(f"### Test Your Knowledge - {len(mcqs)} Questions")
st.html("<div class='info-strip'>Select one answer per question, then submit the quiz.</div>")

with st.form("quiz_form"):
    user_answers = {}
    for i, mcq in enumerate(mcqs):
        opts = [mcq.get("option_a", ""), mcq.get("option_b", ""), mcq.get("option_c", ""), mcq.get("option_d", "")]
        opts = [o for o in opts if o.strip()]

        st.html(
            f"""
            <div class="quiz-question">
                <strong style="color:#1769e0;">Q{i + 1}:</strong>
                <span style="color:#42546f;">{html.escape(mcq['question'])}</span>
            </div>
            """
        )
        user_answers[i] = st.radio(
            f"q_{i + 1}",
            options=opts,
            key=f"q_{i}",
            label_visibility="collapsed",
            index=None,
        )
        st.write("")

    submitted = st.form_submit_button("Submit Quiz")

if submitted:
    missing = [i + 1 for i in range(len(mcqs)) if user_answers.get(i) is None]
    if missing:
        st.error(f"Please answer all questions before submitting. Missing questions: {', '.join(map(str, missing))}")
        st.stop()

    score = sum(1 for i, mcq in enumerate(mcqs) if user_answers.get(i) == mcq.get("correct_answer"))
    total = len(mcqs)
    pct = score / total * 100 if total > 0 else 0

    save_quiz_result(selected_id, score, total)

    st.markdown("---")
    st.markdown("### Your Result")
    st.html(score_badge_html(score, total))
    st.write("")

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=pct,
            number={"suffix": "%", "font": {"size": 36, "color": "#10233f", "family": "Inter"}},
            gauge={
                "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#9fb4d1"},
                "bar": {"color": "#1769e0"},
                "bgcolor": "#ffffff",
                "borderwidth": 0,
                "steps": [
                    {"range": [0, 60], "color": "#fff7ed"},
                    {"range": [60, 80], "color": "#eaf4ff"},
                    {"range": [80, 100], "color": "#edfdf8"},
                ],
                "threshold": {"line": {"color": "#2f8cff", "width": 3}, "thickness": 0.85, "value": pct},
            },
            title={"text": "Score", "font": {"color": "#5f728f", "size": 14}},
        )
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        height=260,
        margin=dict(l=20, r=20, t=20, b=20),
        font=dict(family="Inter"),
    )
    _, gauge_col, _ = st.columns([1, 3, 1])
    with gauge_col:
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    with st.expander("Review Answers", expanded=True):
        for i, mcq in enumerate(mcqs):
            correct = mcq.get("correct_answer", "")
            chosen = user_answers.get(i, "")
            is_right = chosen == correct
            cls = "ok" if is_right else "bad"
            label = "Correct" if is_right else "Needs review"

            st.html(
                f"""
                <div class="review-card {cls}">
                    <strong>{label} - Q{i + 1}: {html.escape(mcq['question'])}</strong><br>
                    <span style="color:#5f728f;">Your answer: </span>
                    <strong>{html.escape(chosen)}</strong>
                    {"" if is_right else f"<br><span style='color:#5f728f;'>Correct answer: </span><strong>{html.escape(correct)}</strong>"}
                </div>
                """
            )

    if st.button("Regenerate Questions"):
        text_path = os.path.join(os.path.dirname(__file__), "..", "uploads", "texts", f"{selected_id}.txt")
        if os.path.exists(text_path):
            with st.spinner("Generating new questions..."):
                with open(text_path, "r", encoding="utf-8") as f:
                    text = f.read()
                new_mcqs = generate_mcqs(text, num_mcqs=len(mcqs))
                save_mcqs(selected_id, new_mcqs)
            st.success("New questions generated.")
            st.rerun()
