import streamlit as st

st.set_page_config(page_title="SongBridge", page_icon="🎵", layout="centered")

# ── a tiny bit of styling ──────────────────────────────────────
st.markdown("""
<style>
    .block-container { padding-top: 2rem; max-width: 700px; }
    div[data-testid="stSelectbox"] > label { font-weight: 500; }
</style>
""", unsafe_allow_html=True)

# ── session state ──────────────────────────────────────────────────────────────
if "song1" not in st.session_state:
    st.session_state.song1 = None
if "song2" not in st.session_state:
    st.session_state.song2 = None
if "n_bridge" not in st.session_state:
    st.session_state.n_bridge = 3
if "show_result" not in st.session_state:
    st.session_state.show_result = False

# ── placeholder songs  ─────────────────────────────────
SONGS = ["Song 1", "Song 2", "Song 3", "Song 4", "Song 5", "Song 6"]

# ── callbacks ──────────────────────────────────────────────────────────────────
def on_select1():
    st.session_state.song1 = st.session_state._sel1
    st.session_state.show_result = False

def on_select2():
    st.session_state.song2 = st.session_state._sel2
    st.session_state.show_result = False

def increment():
    if st.session_state.n_bridge < 5:
        st.session_state.n_bridge += 1
    st.session_state.show_result = False

def decrement():
    if st.session_state.n_bridge > 1:
        st.session_state.n_bridge -= 1
    st.session_state.show_result = False

def find_bridges():
    st.session_state.show_result = True

def reset():
    st.session_state.song1 = None
    st.session_state.song2 = None
    st.session_state.n_bridge = 3
    st.session_state.show_result = False

# ── header ─────────────────────────────────────────────────────────────────────
st.title("SongBridge")
st.caption("Pick two songs — the AI finds what goes in between.")
st.divider()

# ── song selectors ─────────────────────────────────────────────────────────────
col1, col2 = st.columns(2, gap="medium")

with col1:
    st.markdown("####  First Song")
    options1 = [s for s in SONGS if s != st.session_state.song2]
    st.selectbox(
        "Choose your first song",
        options=["-- select --"] + options1,
        key="_sel1",
        on_change=on_select1,
        label_visibility="collapsed",
    )
    if st.session_state.song1 and st.session_state.song1 != "-- select --":
        st.success(f"✅  **{st.session_state.song1}** selected")
    else:
        st.caption("No song selected yet")

with col2:
    st.markdown("####  Second Song")
    options2 = [s for s in SONGS if s != st.session_state.song1]
    st.selectbox(
        "Choose your second song",
        options=["-- select --"] + options2,
        key="_sel2",
        on_change=on_select2,
        label_visibility="collapsed",
    )
    if st.session_state.song2 and st.session_state.song2 != "-- select --":
        st.success(f"  **{st.session_state.song2}** selected")
    else:
        st.caption("No song selected yet")

st.divider()

# ── bridge count ───────────────────────────────────────────────────────────────
st.markdown("####  How many bridge songs?")
st.caption("Adjust how many songs the AI will suggest to connect your two tracks.")

left, mid, right = st.columns([1, 1, 4], gap="small")
with left:
    st.button("  ➖  ", on_click=decrement, use_container_width=True)
with mid:
    st.button("  ➕  ", on_click=increment, use_container_width=True)
with right:
    st.markdown(
        f"<p style='padding-top:8px; font-size:15px;'>"
        f"<b>{st.session_state.n_bridge}</b> bridge song{'s' if st.session_state.n_bridge > 1 else ''}</p>",
        unsafe_allow_html=True,
    )

st.divider()

# ── find button ────────────────────────────────────────────────────────────────
both_ready = (
    st.session_state.song1 not in (None, "-- select --")
    and st.session_state.song2 not in (None, "-- select --")
)

if not both_ready:
    st.warning("Please Select both songs above before continuing.")

st.button(
    "  Find Bridge Songs",
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

    # playlist display
    cols = st.columns([1, 6])
    with cols[0]: st.markdown("▶")
    with cols[1]: st.markdown(f"**{st.session_state.song1}** — *start*")

    for i in range(st.session_state.n_bridge):
        cols = st.columns([1, 6])
        with cols[0]: st.markdown("🎵")
        with cols[1]: st.markdown(f"Bridge Song {i + 1}")

    cols = st.columns([1, 6])
    with cols[0]: st.markdown("▶")
    with cols[1]: st.markdown(f"**{st.session_state.song2}** — *end*")

    st.write("")
    st.button("Start Over", on_click=reset, use_container_width=True)