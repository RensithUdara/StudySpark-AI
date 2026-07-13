import html
import os
import random

import streamlit as st

from database.database import get_all_lectures, get_flashcards, save_flashcards
from models.flashcard_generator import create_flashcards
from utils.styles import inject_css, page_header

inject_css()
page_header("Flashcards", "Practice active recall with AI-generated question and answer cards.")

lectures = get_all_lectures()
if not lectures:
    st.warning("No lectures found. Please upload a lecture first.")
    st.stop()

options = {lec["id"]: lec["title"] for lec in lectures}
selected_id = st.selectbox("Select lecture", options=list(options.keys()), format_func=lambda x: options[x])

flashcards = get_flashcards(selected_id)

if not flashcards:
    st.info("No flashcards found for this lecture.")
    num_cards = st.slider("How many flashcards to generate?", 4, 15, 8)
    if st.button("Generate Flashcards"):
        text_path = os.path.join(os.path.dirname(__file__), "..", "uploads", "texts", f"{selected_id}.txt")
        if os.path.exists(text_path):
            with st.spinner("Generating flashcards using AI..."):
                with open(text_path, "r", encoding="utf-8") as f:
                    text = f.read()
                new_fcs = create_flashcards(text, num_cards=num_cards)
                save_flashcards(selected_id, new_fcs)
            st.success(f"{len(new_fcs)} flashcards generated.")
            st.rerun()
        else:
            st.error("Source text not found. Please re-upload the lecture.")
    st.stop()

if "fc_lecture" not in st.session_state or st.session_state.fc_lecture != selected_id:
    st.session_state.fc_lecture = selected_id
    st.session_state.fc_index = 0
    st.session_state.fc_flipped = False
    st.session_state.fc_known = set()
    st.session_state.fc_review = set()
    st.session_state.fc_order = list(range(len(flashcards)))

order = st.session_state.get("fc_order", list(range(len(flashcards))))
idx = st.session_state.fc_index
total = len(flashcards)
current_fc = flashcards[order[idx]]
known_set = st.session_state.fc_known
review_set = st.session_state.fc_review

answered = len(known_set) + len(review_set)
pct = int(answered / total * 100)
st.html(
    f"""
    <div class="progress-meta">
        <span>Card <strong>{idx + 1}</strong> of {total}</span>
        <span><strong style="color:#087f5b;">{len(known_set)} known</strong> |
        <strong style="color:#b45309;">{len(review_set)} review</strong></span>
    </div>
    <div class="progress-track"><div class="progress-fill" style="width:{pct}%;"></div></div>
    """
)

_, card_col, _ = st.columns([1, 7, 1])
with card_col:
    if not st.session_state.fc_flipped:
        st.html(
            f"""
            <div class="flashcard-face flashcard-front">
                <div class="fc-label">QUESTION</div>
                <div class="fc-text">{html.escape(current_fc['question'])}</div>
            </div>
            <div class="muted-hint">Reveal the answer when you are ready.</div>
            """
        )
    else:
        st.html(
            f"""
            <div class="flashcard-face flashcard-back">
                <div class="fc-label">ANSWER</div>
                <div class="fc-text">{html.escape(current_fc['answer'])}</div>
            </div>
            """
        )

st.write("")
_, btn_col, _ = st.columns([2, 4, 2])
with btn_col:
    flip_label = "Reveal Answer" if not st.session_state.fc_flipped else "Back to Question"
    if st.button(flip_label, use_container_width=True):
        st.session_state.fc_flipped = not st.session_state.fc_flipped
        st.rerun()

if st.session_state.fc_flipped:
    st.write("")
    ka_col, ra_col = st.columns(2)
    with ka_col:
        if st.button("I Know This", use_container_width=True, help="Mark this card as learned"):
            known_set.add(order[idx])
            review_set.discard(order[idx])
            st.session_state.fc_known = known_set
            st.session_state.fc_review = review_set
            if idx < total - 1:
                st.session_state.fc_index = idx + 1
                st.session_state.fc_flipped = False
            st.rerun()
    with ra_col:
        if st.button("Review Again", use_container_width=True, help="Mark for further review"):
            review_set.add(order[idx])
            known_set.discard(order[idx])
            st.session_state.fc_known = known_set
            st.session_state.fc_review = review_set
            if idx < total - 1:
                st.session_state.fc_index = idx + 1
                st.session_state.fc_flipped = False
            st.rerun()

st.markdown("---")

nav1, nav2, nav3 = st.columns(3)
with nav1:
    if st.button("Previous", use_container_width=True, disabled=(idx == 0)):
        st.session_state.fc_index = idx - 1
        st.session_state.fc_flipped = False
        st.rerun()
with nav2:
    if st.button("Shuffle", use_container_width=True):
        shuffled = list(range(total))
        random.shuffle(shuffled)
        st.session_state.fc_order = shuffled
        st.session_state.fc_index = 0
        st.session_state.fc_flipped = False
        st.rerun()
with nav3:
    if st.button("Next", use_container_width=True, disabled=(idx == total - 1)):
        st.session_state.fc_index = idx + 1
        st.session_state.fc_flipped = False
        st.rerun()

with st.expander("Regenerate Flashcards"):
    num_new = st.slider("Number of cards", 4, 15, 8, key="fc_regen_n")
    if st.button("Regenerate", use_container_width=True, key="fc_regen_btn"):
        text_path = os.path.join(os.path.dirname(__file__), "..", "uploads", "texts", f"{selected_id}.txt")
        if os.path.exists(text_path):
            with st.spinner("Regenerating flashcards..."):
                with open(text_path, "r", encoding="utf-8") as f:
                    text = f.read()
                new_fcs = create_flashcards(text, num_cards=num_new)
                save_flashcards(selected_id, new_fcs)
            st.success("Flashcards regenerated.")
            st.session_state.fc_index = 0
            st.session_state.fc_flipped = False
            st.session_state.fc_known = set()
            st.session_state.fc_review = set()
            st.session_state.fc_order = list(range(len(new_fcs)))
            st.rerun()
