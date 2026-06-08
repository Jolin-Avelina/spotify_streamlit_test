

import streamlit as st
from difflib import SequenceMatcher
import pickle
from time import time
from pyinstrument import Profiler

profiler = Profiler()
profiler.start()



st.set_page_config(page_title="SongBridge", page_icon="🎵", layout="centered")

st.markdown("""
<style>
    .block-container { padding-top: 2rem; max-width: 700px; }
</style>
""", unsafe_allow_html=True)

# ── session state ──────────────────────────────────────────────────────────────
defaults = {
    "song1": None,
    "song2": None,
    "n_bridge": 3,
    "show_result": False,
    "bridge_results":[]
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

bridge_list=[]

# ── placeholder songs (replace with DB later) ─────────────────────────────────\

# call config_filename
@st.cache_resource(ttl=24*60*60)
def importlist():
    ALL_SONGS = pickle.load(open('pickle/mylist_smaller.pkl','rb'))
    return ALL_SONGS

@st.cache_resource
def importall():
    df = pickle.load(open('pickle/df_smaller.pkl','rb'))
    X_scaled = pickle.load(open('pickle/X_scaled_smaller.pkl','rb'))
    knn = pickle.load(open('pickle/knn_smaller.pkl','rb'))
    return df,X_scaled,knn
df,X_scaled,knn=importall()


ALL_SONGS=importlist()
# print("Data loaded from file:")


# ALL_SONGS = [
#     "Blinding Lights", "Shape of You", "Someone Like You", "Bohemian Rhapsody", "Stay",
# "Bad Guy", "Thinking Out Loud", "Rolling in the Deep", "Levitating", "Uptown Funk",
# ]

# ── callbacks ──────────────────────────────────────────────────────────────────

def on_select1():
    val = st.session_state._sel1
    st.session_state.song1 = val if val != "-- select a song --" else None
    st.session_state.show_result = False

def on_select2():
    val = st.session_state._sel2
    st.session_state.song2 = val if val != "-- select a song --" else None
    st.session_state.show_result = False

def increment():
    if st.session_state.n_bridge < 5:
        st.session_state.n_bridge += 1
    st.session_state.show_result = False


def decrement():
    if st.session_state.n_bridge > 1:
        st.session_state.n_bridge -= 1
    st.session_state.show_result = False

start_uncached_3=time()
def find_bridges():
    #get a list
    start_uncached_3 = time()
    song1=st.session_state.song1
    song2=st.session_state.song2
    results = bridge_recommendation(song1, song2, st.session_state.n_bridge)
    normalized_results = normalize_scores(results)

    st.session_state.bridge_results=normalized_results
    #store in session state
    st.session_state.show_result = True

def reset():
    for k, v in defaults.items():
        st.session_state[k] = v


# ── header ─────────────────────────────────────────────────────────────────────
st.title("SongBridge")
st.caption("Search for two songs — the AI finds what goes in between.")
st.divider()

# ── song search boxes ──────────────────────────────────────────────────────────
st.caption("Tip: click the dropdown and start typing to search — no need to press Enter.")

col1, col2 = st.columns(2, gap="medium")

start_uncached_1 = time()
with col1:
    st.markdown("#### First Song")
    options1 = ["-- select a song --"] + [s for s in ALL_SONGS if s != st.session_state.song2]
    st.selectbox(
        "First Song",
        options=options1,
        key="_sel1",
        on_change=on_select1,
        label_visibility="collapsed",
    )
    if st.session_state.song1:
        st.success(f"Selected: **{st.session_state.song1}**")
load_uncached_1 = time()

start_uncached_2 = time()
with col2:
    st.markdown("#### Second Song")
    options2 = ["-- select a song --"] + [s for s in ALL_SONGS if s != st.session_state.song1]
    st.selectbox(
        "Second Song",
        options=options2,
        key="_sel2",
        on_change=on_select2,
        label_visibility="collapsed",
    )
    if st.session_state.song2:
        st.success(f"Selected: **{st.session_state.song2}**")
load_uncached_2 = time()

benchmark_uncached = (
    f"First one {load_uncached_1 - start_uncached_1:.2f}s "
    f"Second one {load_uncached_2 - start_uncached_2:.2f}"
)

st.text(benchmark_uncached)


st.divider()

# ── bridge count ───────────────────────────────────────────────────────────────
st.markdown("#### How many bridge songs?")
st.caption("Adjust how many songs the AI will suggest to connect your two tracks.")

# left, mid, right = st.columns([1, 1, 4], gap="small")
# with left:
#     st.button("Less", on_click=decrement, use_container_width=True)
# with mid:
#     st.button("More", on_click=increment, use_container_width=True)
# with right:
#     st.markdown(
#         f"<p style='padding-top:8px; font-size:15px;'>"
#         f"<b>{st.session_state.n_bridge}</b> bridge song{'s' if st.session_state.n_bridge > 1 else ''}</p>",
#         unsafe_allow_html=True,
#     )
st.session_state.n_bridge = st.slider("", 3, 10, 4)
st.divider()
from main import *

# ── find button ────────────────────────────────────────────────────────────────
both_ready = st.session_state.song1 is not None and st.session_state.song2 is not None

if not both_ready:
    st.warning("Select both songs above before continuing.")

st.button(
    "Find Bridge Songs",
    on_click=find_bridges,
    disabled=not both_ready,
    use_container_width=True,
    type="primary",
)

# ── result ─────────────────────────────────────────────────────────────────────
if st.session_state.show_result and both_ready:

    st.divider()
    st.markdown("#### Your Bridge Playlist")
    st.caption(
        "These songs are chosen by the AI to smoothly transition "
        "from your first song to your second using tempo, key, and mood."
    )

    st.write("")

    cols = st.columns([1, 6])
    with cols[0]: st.markdown("▶")
    with cols[1]: st.markdown(f"**{st.session_state.song1}** — start")

    # for i in range(st.session_state.n_bridge):
    #     cols = st.columns([1, 6])
    #     with cols[0]: st.markdown("—")
    #     with cols[1]: st.markdown(f"{st.session_state.bridge_results[i]}")
    for name, score, confidence in st.session_state.bridge_results:
        cols = st.columns([1, 6])
        with cols[0]: st.markdown("—")
        with cols[1]: st.markdown(f"{name}")

    cols = st.columns([1, 6])
    with cols[0]: st.markdown("▶")
    with cols[1]: st.markdown(f"**{st.session_state.song2}** — end")
    end_uncached_3 = time()
    st.write("")
    benchmark_uncached_2 = (
        f"Load time {end_uncached_3 - start_uncached_3:.2f}s "
    )
    st.text(benchmark_uncached_2)
    st.write("After using the app at least once, please fill the form below!")
    st.write("https://forms.gle/HNqYHZuc5TZEyatN9")
    st.button("Start Over", on_click=reset, use_container_width=True)
    
    # code you want to profile
    profiler.stop()
    profiler.print()
