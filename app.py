from pathlib import Path

import pandas as pd
import streamlit as st


DATA_PATH = Path(__file__).parent / "data" / "words_to_learn.csv"


@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)


def init_word_index():
    if "word_index" not in st.session_state:
        st.session_state.word_index = 0


def reinit_word_index():
    if "word_index" in st.session_state:
        st.session_state.word_index = 0


def known_words_state():
    if "known" not in st.session_state:
        st.session_state.known = 0


def reinit_known_state():
    if "known" in st.session_state:
        st.session_state.known = 0


def unknown_words_state():
    if "unknown_list" not in st.session_state:
        st.session_state.unknown_list = []


def reinit_unknown_words_state():
    if "unknown_list" in st.session_state:
        st.session_state.unknown_list = []


st.title("Fiszki")
data = load_data()

words = st.empty()
total = len(list(data.index))
init_word_index()
known_words_state()
unknown_words_state()
if st.session_state.word_index > len(list(data.index)) - 1:
    st.write(f"You know {st.session_state.known} out of {total} words")
    if st.session_state.unknown_list:
        st.write(f"The words you didn't know: **{', '.join(st.session_state.unknown_list)}**")
    else:
        st.write("Congrats! :tada: You know all the words!")
    restart = st.button("Restart")
    if restart:
        reinit_word_index()
        reinit_known_state()
        reinit_unknown_words_state()
else:
    word = data.at[st.session_state.word_index, "French"]
    with words.container():
        st.write("Do you know this word?")
        _, c2, _ = st.columns(3)
        with c2:
            st.header(f"**{word}**")
        _, col1, _, _, col2, _ = st.columns(6)
        with col1:
            no_button = st.button("No", key=f"No")
        with col2:
            yes_button = st.button("Yes", key=f"Yes")
        if yes_button:
            st.write("Bravo!")
            st.session_state.known += 1
            st.session_state.word_index += 1
        elif no_button:
            prev_french_word = data.at[max(0, st.session_state.word_index - 1), "French"]
            english_word = data.at[max(0, st.session_state.word_index - 1), "English"]
            st.write(f"You will need to go back to this word.")
            with st.expander("Show previous word translation"):
                st.write(f"**{prev_french_word}** is in English: **{english_word}**")
            st.session_state.unknown_list.append(word)
            st.session_state.word_index += 1
        else:
            st.stop()
