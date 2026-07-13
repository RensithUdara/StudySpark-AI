import html
import os

import pandas as pd
import plotly.express as px
import streamlit as st

from database.database import (
    delete_lecture,
    get_all_lectures,
    get_all_quiz_results,
    get_flashcards_count,
    get_lecture_count,
    get_mcq_count,
    get_notes_count,
)
from utils.styles import inject_css, page_header

inject_css()
page_header("Learning Dashboard", "Track study content, generated resources, and quiz performance.")

def safe_plotly_chart(fig, fallback_message: str):
    """Render a chart without exposing raw tracebacks to app users."""
    try:
        st.plotly_chart(fig, use_container_width=True)
    except Exception:
        st.warning(fallback_message)


try:
    lec_count = get_lecture_count()
    fc_count = get_flashcards_count()
    mcq_count = get_mcq_count()
    notes_count = get_notes_count()
    lectures = get_all_lectures()
except Exception:
    st.error("Dashboard data could not be loaded. Please restart the app or check the local database.")
    st.stop()

total_words = sum(lec.get("word_count", 0) for lec in lectures)
reading_mins = max(0, round(total_words / 200))

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Lectures", lec_count)
c2.metric("Note Sets", notes_count)
c3.metric("Flashcards", fc_count)
c4.metric("MCQs", mcq_count)
c5.metric("Reading Saved", f"{reading_mins} min", help="Estimated reading time from all uploaded lectures")

st.markdown("---")

col_left, col_right = st.columns(2)

with col_left:
    st.markdown("### Content Overview")
    df = pd.DataFrame(
        {
            "Resource": ["Lectures", "Notes", "Flashcards", "MCQs"],
            "Count": [lec_count, notes_count, fc_count, mcq_count],
        }
    )
    fig = px.bar(
        df,
        x="Resource",
        y="Count",
        color="Resource",
        color_discrete_map={
            "Lectures": "#0b5bd3",
            "Notes": "#1769e0",
            "Flashcards": "#2f8cff",
            "MCQs": "#73b7ff",
        },
        template="plotly_white",
        title="Generated Resources",
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#ffffff",
        showlegend=False,
        font=dict(family="Inter", color="#42546f"),
        title_font=dict(size=15, color="#10233f"),
        margin=dict(l=10, r=10, t=40, b=10),
        xaxis=dict(title="", gridcolor="#e3efff"),
        yaxis=dict(title="Count", gridcolor="#e3efff"),
    )
    fig.update_traces(marker_line_width=0)
    safe_plotly_chart(fig, "Content overview chart is temporarily unavailable.")

with col_right:
    st.markdown("### Quiz Performance")
    try:
        all_results = get_all_quiz_results()
    except Exception:
        all_results = []
        st.warning("Quiz performance could not be loaded right now.")
    if all_results:
        df_quiz = pd.DataFrame(all_results)
        df_quiz["Score (%)"] = (df_quiz["score"] / df_quiz["total_questions"] * 100).round(1)
        df_quiz["Lecture"] = df_quiz["lecture_title"].apply(lambda t: t[:22] + "..." if len(t) > 22 else t)
        df_quiz["Date"] = pd.to_datetime(df_quiz["taken_at"]).dt.strftime("%b %d")

        fig2 = px.line(
            df_quiz,
            x="Date",
            y="Score (%)",
            color="Lecture",
            markers=True,
            template="plotly_white",
            title="Quiz Scores Over Time",
            line_shape="spline",
        )
        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="#ffffff",
            font=dict(family="Inter", color="#42546f"),
            title_font=dict(size=15, color="#10233f"),
            margin=dict(l=10, r=10, t=40, b=10),
            colorway=["#0b5bd3", "#1769e0", "#2f8cff", "#73b7ff", "#0b2a5f"],
            yaxis=dict(range=[0, 105], gridcolor="#e3efff", title="Score %"),
            xaxis=dict(gridcolor="#e3efff"),
        )
        fig2.update_traces(line_width=2.5, marker_size=7)
        safe_plotly_chart(fig2, "Quiz performance chart is temporarily unavailable.")
    else:
        st.info("Take a quiz to see your performance history here.")

try:
    all_results = get_all_quiz_results()
except Exception:
    all_results = []
if all_results:
    st.markdown("---")
    st.markdown("### Quiz History")
    df_hist = pd.DataFrame(all_results)
    df_hist["Score (%)"] = (df_hist["score"] / df_hist["total_questions"] * 100).round(1)
    df_hist["Grade"] = df_hist["Score (%)"].apply(
        lambda p: "Excellent" if p >= 80 else ("Good" if p >= 60 else "Review")
    )
    df_hist["Date"] = pd.to_datetime(df_hist["taken_at"]).dt.strftime("%Y-%m-%d %H:%M")
    display_cols = ["lecture_title", "score", "total_questions", "Score (%)", "Grade", "Date"]
    df_hist = df_hist[display_cols].rename(
        columns={"lecture_title": "Lecture", "score": "Score", "total_questions": "Total Qs"}
    )
    st.dataframe(df_hist, use_container_width=True, hide_index=True)

if lectures:
    st.markdown("---")
    st.markdown("### Uploaded Lectures")
    for lec in lectures:
        with st.container():
            col_info, col_del = st.columns([8, 0.7], vertical_alignment="center")
            with col_info:
                title = html.escape(str(lec["title"]))
                st.html(
                    f"""
                    <div class="info-strip lecture-row">
                        <strong class="lecture-title">{title}</strong>
                        <small>
                            {lec.get('pages', 0)} pages | {lec.get('word_count', 0):,} words |
                            Uploaded {lec.get('upload_date', '')[:10]}
                        </small>
                    </div>
                    """
                )
            with col_del:
                if st.button("Delete", key=f"del_{lec['id']}", help="Delete this lecture and all its data"):
                    text_path = os.path.join(
                        os.path.dirname(__file__), "..", "uploads", "texts", f"{lec['id']}.txt"
                    )
                    if os.path.exists(text_path):
                        os.remove(text_path)
                    delete_lecture(lec["id"])
                    st.success(f"Deleted '{lec['title']}'")
                    st.rerun()
