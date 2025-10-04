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
    if "idx" not in st.session_state:
        st.session_state.idx = 0
    if "revealed" not in st.session_state:
        st.session_state.revealed = False

def clamp_idx():
    n = len(st.session_state.deck)
    if n == 0:
        st.session_state.idx = 0
    else:
        st.session_state.idx %= n

init_state()
clamp_idx()

# ---------- Callbacks (use stable keys to avoid double-click/skips) ----------
def on_prev():
    if not st.session_state.deck:
        return
    st.session_state.idx = (st.session_state.idx - 1) % len(st.session_state.deck)
    st.session_state.revealed = False

def on_next():
    if not st.session_state.deck:
        return
    st.session_state.idx = (st.session_state.idx + 1) % len(st.session_state.deck)
    st.session_state.revealed = False

def on_shuffle():
    if not st.session_state.deck:
        return
    random.shuffle(st.session_state.deck)
    st.session_state.idx = 0
    st.session_state.revealed = False

def on_toggle_reveal():
    st.session_state.revealed = not st.session_state.revealed

# ---------- UI ----------
st.title("IELTS speaking grammar helper")
st.subheader("Countable vs Uncountable · Flashcards")

if not st.session_state.deck:
    st.info("No cards available. Add 'countabilityCards' to data.json.")
    st.stop()

card = st.session_state.deck[st.session_state.idx]

# Word face
st.markdown(
    f'<div style="font-size:44px;font-weight:800;letter-spacing:.3px">{card.get("word","")}</div>',
    unsafe_allow_html=True,
)
st.caption("Reveal shows countability and example. Prev/Next always hide by default.")

# Controls: Prev · Reveal/Hide · Next · Shuffle · Counter
c1, c2, c3, c4, c5 = st.columns([1, 1, 1, 1, 3])
with c1:
    st.button("◀ Prev", key="btn_prev", on_click=on_prev)
with c2:
    label = "Hide" if st.session_state.revealed else "Reveal"
    st.button(label, key="btn_toggle", on_click=on_toggle_reveal)
with c3:
    st.button("Next ▶", key="btn_next", on_click=on_next)
with c4:
    st.button("Shuffle", key="btn_shuffle", on_click=on_shuffle)
with c5:
    st.write(f"{st.session_state.idx + 1} / {len(st.session_state.deck)}")

# Reveal panel
if st.session_state.revealed:
    typ = (card.get("countability") or "").lower()
    color = {"countable": "#16a34a", "uncountable": "#dc2626", "both": "#2563eb"}.get(typ, "#6b7280")

    st.markdown(
        f"""<span style="display:inline-block;padding:4px 10px;border-radius:9999px;
        font-size:12px;font-weight:600;color:white;background:{color};">{typ or "unknown"}</span>""",
        unsafe_allow_html=True,
    )

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
