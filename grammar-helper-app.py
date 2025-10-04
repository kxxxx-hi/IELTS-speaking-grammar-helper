import json
import random
from pathlib import Path
import streamlit as st

# ---------------- App setup ----------------
st.set_page_config(page_title="IELTS speaking grammar helper", layout="wide")

DATA_PATH = Path("data.json")
try:
    DATA = json.loads(DATA_PATH.read_text(encoding="utf-8")) if DATA_PATH.exists() else {}
except Exception:
    DATA = {}

CARDS = DATA.get("countabilityCards", [])

# ---------------- State + helpers ----------------
def init_state():
    if "deck" not in st.session_state:
        st.session_state.deck = list(CARDS)
        st.session_state.idx = 0
        st.session_state.revealed = False

def goto(delta: int):
    n = len(st.session_state.deck)
    if n == 0:
        return
    st.session_state.idx = (st.session_state.idx + delta) % n
    st.session_state.revealed = False

def shuffle_deck():
    random.shuffle(st.session_state.deck)
    st.session_state.idx = 0
    st.session_state.revealed = False

def current_card():
    if not st.session_state.deck:
        return None
    return st.session_state.deck[st.session_state.idx]

def badge(text, color):
    st.markdown(
        f"""<span style="display:inline-block;padding:4px 10px;border-radius:9999px;
        font-size:12px;font-weight:600;color:white;background:{color};">{text}</span>""",
        unsafe_allow_html=True,
    )

init_state()

# ---------------- Tabs ----------------
tab1, tab2, tab3 = st.tabs([
    "Countability Flashcards",
    "Listening / Vocab (future)",
    "More Tools (future)"
])

with tab1:
    st.subheader("Countable vs Uncountable · Flashcards")

    left, mid, right = st.columns([2, 3, 2])

    with left:
        st.caption("Options")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Shuffle deck"):
                shuffle_deck()
        with c2:
            upload = st.file_uploader("Load custom data.json", type=["json"], label_visibility="collapsed")
            if upload:
                try:
                    data2 = json.loads(upload.read().decode("utf-8"))
                    cards2 = data2.get("countabilityCards", [])
                    if isinstance(cards2, list) and cards2:
                        st.session_state.deck = cards2
                        st.session_state.idx = 0
                        st.session_state.revealed = False
                        st.success("Loaded custom countabilityCards from data.json.")
                    else:
                        st.error("Invalid JSON: missing non-empty 'countabilityCards' array.")
                except Exception as e:
                    st.error(f"Failed to parse JSON: {e}")

        kinds = ["countable", "uncountable", "both"]
        picked = st.multiselect("Filter by type", kinds, default=kinds)
        if picked and CARDS:
            st.session_state.deck = [c for c in CARDS if c.get("countability") in picked]
            st.session_state.idx = 0
            st.session_state.revealed = False

    with mid:
        card = current_card()
        if not st.session_state.deck:
            st.info("No cards available. Add 'countabilityCards' to data.json.")
        else:
            st.markdown(
                """
                <div style="border:1px solid #e5e7eb;border-radius:16px;padding:30px 20px;
                text-align:center;background:#fafafa;min-height:220px;display:flex;
                align-items:center;justify-content:center;flex-direction:column;">
                """,
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<div style="font-size:40px;font-weight:800;letter-spacing:0.5px">{card.get("word","")}</div>',
                unsafe_allow_html=True,
            )
            st.caption("Click “Reveal” to show countability and an example.")
            st.markdown("</div>", unsafe_allow_html=True)

            c1, c2, c3, c4 = st.columns([1, 1, 1, 3])
            with c1:
                if st.button("◀ Prev"):
                    goto(-1)
            with c2:
                if st.button("Reveal" if not st.session_state.revealed else "Hide"):
                    st.session_state.revealed = not st.session_state.revealed
            with c3:
                if st.button("Next ▶"):
                    goto(+1)
            with c4:
                st.write(f"{st.session_state.idx + 1} / {len(st.session_state.deck)}")

            if st.session_state.revealed:
                typ = (card.get("countability") or "").lower()
                color = {"countable": "#16a34a", "uncountable": "#dc2626", "both": "#2563eb"}.get(typ, "#6b7280")
                badge(typ or "unknown", color)

                ex = card.get("example") or ""
                if ex:
                    st.markdown(
                        f"""
                        <div style="margin-top:14px;border-left:4px solid {color};
                        padding:10px 14px;background:white;border-radius:10px;">
                          <div style="font-size:14px;color:#6b7280;margin-bottom:4px;">Example</div>
                          <div style="font-size:18px;font-weight:600;">{ex}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                tip = card.get("tip")
                if tip:
                    st.caption(tip)

    with right:
        st.caption("Jump to")
        if st.session_state.deck:
            names = [c.get("word", "") for c in st.session_state.deck]
            target = st.selectbox("Pick a word", options=names, index=st.session_state.idx)
            if st.button("Go"):
                st.session_state.idx = names.index(target)
                st.session_state.revealed = False

with tab2:
    st.info("Reserve this tab for pronunciation, minimal pairs, or antonyms later.")

with tab3:
    st.info("Add more IELTS helpers here later (e.g., collocations, topic wheels).")
