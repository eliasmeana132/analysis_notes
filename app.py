import streamlit as st
import json
import os
import random

st.set_page_config(page_title="Math Analysis Memorizer", layout="centered")

@st.cache_data
def load_cards():
    cards = []
    data_dir = "data"
    if not os.path.exists(data_dir):
        return cards
        
    chapter_files = [f for f in os.listdir(data_dir) if f.endswith(".json")]
    for file in sorted(chapter_files):
        with open(os.path.join(data_dir, file), "r", encoding="utf-8") as f:
            chapter_data = json.load(f)
            cards.extend(chapter_data)
    return cards

cards = load_cards()

if not cards:
    st.error("No flashcards found. Please add chapter JSON files to the 'data' folder.")
    st.stop()

if 'index' not in st.session_state:
    st.session_state.index = 0
if 'show_answer' not in st.session_state:
    st.session_state.show_answer = False

st.title("Math Analysis Memorizer")

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Previous", use_container_width=True):
        st.session_state.index = max(0, st.session_state.index - 1)
        st.session_state.show_answer = False
with col2:
    if st.button("Shuffle", use_container_width=True):
        random.shuffle(cards)
        st.session_state.index = 0
        st.session_state.show_answer = False
with col3:
    if st.button("Next", use_container_width=True):
        st.session_state.index = min(len(cards) - 1, st.session_state.index + 1)
        st.session_state.show_answer = False

st.progress((st.session_state.index + 1) / len(cards))
st.caption(f"Card {st.session_state.index + 1} of {len(cards)}")

card = cards[st.session_state.index]

with st.container(border=True):
    st.caption(card.get("type", "Result"))
    st.markdown(f"### {card.get('concept', '')}")
    
    if st.button("Show / Hide Content", type="primary"):
        st.session_state.show_answer = not st.session_state.show_answer
        
    if st.session_state.show_answer:
        st.divider()
        st.markdown(card.get("content", ""))
