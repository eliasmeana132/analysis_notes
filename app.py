import streamlit as st
import json
import os
import random

st.set_page_config(page_title="Math Analysis Memorizer", layout="centered")

# ---------- Load data (with chapter info) ----------
@st.cache_data
def load_all_cards():
    cards = []
    data_dir = "data"
    if not os.path.exists(data_dir):
        return cards
    chapter_files = [f for f in os.listdir(data_dir) if f.endswith(".json")]
    for file in sorted(chapter_files):
        chapter_name = os.path.splitext(file)[0]
        with open(os.path.join(data_dir, file), "r", encoding="utf-8") as f:
            chapter_data = json.load(f)
            for card in chapter_data:
                card["chapter"] = chapter_name   # tag each card with its chapter
                cards.append(card)
    return cards

# ---------- Helper: original order for a given chapter ----------
def get_original_cards(chapter):
    all_cards = st.session_state.all_cards
    if chapter == "All":
        return list(all_cards)   # return a copy
    else:
        return [card for card in all_cards if card["chapter"] == chapter]

# ---------- Session state initialisation ----------
if "all_cards" not in st.session_state:
    st.session_state.all_cards = load_all_cards()

all_cards = st.session_state.all_cards
if not all_cards:
    st.error("No flashcards found. Please add chapter JSON files to the 'data' folder.")
    st.stop()

# List of available chapters (plus "All")
chapters_list = sorted({card["chapter"] for card in all_cards})
chapters = ["All"] + chapters_list

# Ensure selected_chapter is valid (e.g. after data changes)
if ("selected_chapter" not in st.session_state or
    st.session_state.selected_chapter not in chapters):
    st.session_state.selected_chapter = "All"

if "cards" not in st.session_state:
    st.session_state.cards = get_original_cards(st.session_state.selected_chapter)
if "index" not in st.session_state:
    st.session_state.index = 0
if "show_answer" not in st.session_state:
    st.session_state.show_answer = False

# ---------- Callbacks ----------
def on_chapter_change():
    st.session_state.cards = get_original_cards(st.session_state.selected_chapter)
    st.session_state.index = 0
    st.session_state.show_answer = False

def prev_card():
    if st.session_state.index > 0:
        st.session_state.index -= 1
    st.session_state.show_answer = False

def next_card():
    if st.session_state.index < len(st.session_state.cards) - 1:
        st.session_state.index += 1
    st.session_state.show_answer = False

def shuffle_cards():
    random.shuffle(st.session_state.cards)
    st.session_state.index = 0
    st.session_state.show_answer = False

def reset_cards():
    st.session_state.cards = get_original_cards(st.session_state.selected_chapter)
    st.session_state.index = 0
    st.session_state.show_answer = False

# ---------- UI ----------
st.title("Math Analysis Memorizer")

# Chapter selector
st.selectbox(
    "Chapter",
    chapters,
    key="selected_chapter",
    on_change=on_chapter_change
)

# Guard against empty selection
if not st.session_state.cards:
    st.warning("No cards in this chapter.")
    st.stop()

# Ensure index is within bounds (safety)
st.session_state.index = min(st.session_state.index, len(st.session_state.cards) - 1)

# Navigation & controls
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.button("Previous", on_click=prev_card, use_container_width=True)
with col2:
    st.button("Shuffle", on_click=shuffle_cards, use_container_width=True)
with col3:
    st.button("Next", on_click=next_card, use_container_width=True)
with col4:
    st.button("Reset", on_click=reset_cards, use_container_width=True)

# Progress
total = len(st.session_state.cards)
st.progress((st.session_state.index + 1) / total)
st.caption(f"Card {st.session_state.index + 1} of {total}")

# Current card display
card = st.session_state.cards[st.session_state.index]
with st.container(border=True):
    st.caption(card.get("type", "Result"))
    st.markdown(f"### {card.get('concept', '')}")

    if st.button("Show / Hide Content", type="primary"):
        st.session_state.show_answer = not st.session_state.show_answer

    if st.session_state.show_answer:
        st.divider()
        st.markdown(card.get("content", ""))
