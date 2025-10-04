import json
import random
from pathlib import Path
import streamlit as st

# ---------- App setup ----------
st.set_page_config(page_title="IELTS speaking grammar helper", layout="wide")

DATA_PATH = Path("data.json")
try:
    DATA = json.loads(DATA_PATH.read_text(encoding="utf-8")) if DATA_PATH.exists() else {}
except Exception:
    DATA = {}

CARDS = DATA.get("countabilityCards", [])

# ---------- State ----------
def init_state():
    if "deck" not in st.session_state:
        st.session_state.deck = list(CARDS)
        st.session_state.idx = 0
        st.session_state.revealed = False

def clamp_idx():
    n = len(st.session_state.deck)
    if n == 0:
        st.session_state.idx = 0
        st.session_state.revealed = False
    else:
        st.session_state.idx %= n

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

def badge(text, color):
    st.markdown(
        f"""<span style="display:inline-block;padding:4px 10px;border-radius:9999px;
        font-size:12px;font-weight:600;color:white;background:{color};">{text}</span>""",
        unsafe_allow_html=True,
    )

init_state()
clamp_idx()

# ---------- Single view (no extra tabs/boxes) ----------
st.title("IELTS speaking grammar helper")
st.subheader("Countable vs Uncountable · Flashcards")

if not st.session_state.deck:
    st.info("No cards available. Add 'countabilityCards' to data.json.")
    st.stop()

card = st.session_state.deck[st.session_state.idx]

# Word
st.markdown(
    f'<div style="font-size:44px;font-weight:800;letter-spacing:.3px">{card.get("word","")}</div>',
    unsafe_allow_html=True,
)
st.caption("Click “Reveal” to show countability and an example.")

# Controls row: Prev · Reveal · Next · Shuffle · Counter
c1, c2, c3, c4, c5 = st.columns([1, 1, 1, 1, 3])
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
    if st.button("Shuffle"):
        shuffle_deck()
with c5:
    st.write(f"{st.session_state.idx + 1} / {len(st.session_state.deck)}")

# Reveal panel
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
