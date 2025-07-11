"""
Streamlit front-end for the Groq-powered LangGraph chatbot
----------------------------------------------------------
• Page-1: enter (or generate) session-ID
• Page-2: Hinglish-persona chat, state checkpointed in MongoDB
"""

from __future__ import annotations

import uuid
from typing import Dict, List

import streamlit as st

from checkpointer import get_mongo_checkpointer
from langgraph_flow import build_graph  # ← llm_node already prepends Hinglish prompt


# ──────────────────────────────────────────────────────────────────────────────
# Streamlit global config
# ──────────────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Groq Chatbot", page_icon="💬", layout="centered")


# ──────────────────────────────────────────────────────────────────────────────
# Helper ─ render chat history but hide system messages
# ──────────────────────────────────────────────────────────────────────────────
def render_chat(messages: List[Dict[str, str]]) -> None:
    for msg in messages:
        if msg["role"] == "system":  # never show prompt to user
            continue
        with st.chat_message("assistant" if msg["role"] == "assistant" else "user"):
            st.markdown(msg["content"])


# ──────────────────────────────────────────────────────────────────────────────
# Initialise session-state on first load
# ──────────────────────────────────────────────────────────────────────────────
if "graph" not in st.session_state:
    st.session_state.checkpointer = get_mongo_checkpointer()
    st.session_state.graph = build_graph(st.session_state.checkpointer)
    st.session_state.state: Dict[str, List[Dict[str, str]]] = {"messages": []}
    st.session_state.thread_id: str = ""
    st.session_state.cfg: Dict = {}


# ──────────────────────────────────────────────────────────────────────────────
# PAGE-1: choose / create session ID
# ──────────────────────────────────────────────────────────────────────────────
if st.session_state.thread_id == "":
    st.title("🔑 Start or Resume Session")

    user_input = st.text_input(
        "Enter a session ID (leave blank for a new one):",
        key="session_id_input",
    )

    if st.button("Continue 🚀"):
        # generate or accept given ID
        st.session_state.thread_id = user_input.strip() or str(uuid.uuid4())
        st.session_state.cfg = {"configurable": {"thread_id": st.session_state.thread_id}}

        # attempt to load previous state
        try:
            snapshot = st.session_state.graph.get_state(st.session_state.cfg)
            if snapshot and snapshot.values:
                st.session_state.state = snapshot.values
                st.success("Previous conversation loaded ✅")
        except Exception:
            pass  # will start fresh

        st.rerun()  # switch to chat page

    st.stop()


# ──────────────────────────────────────────────────────────────────────────────
# PAGE-2: chat UI
# ──────────────────────────────────────────────────────────────────────────────
st.title("💬 Chat with Groq-Powered Bot")
st.caption(f"Session ID: `{st.session_state.thread_id}`")

# render history
render_chat(st.session_state.state["messages"])

# input box
prompt = st.chat_input("Type your message and hit Enter …")
if prompt:
    # 1️⃣ append user turn
    st.session_state.state["messages"].append({"role": "user", "content": prompt})

    # 2️⃣ invoke LangGraph → returns updated state (assistant turn included)
    st.session_state.state = st.session_state.graph.invoke(
        st.session_state.state,
        config=st.session_state.cfg,
    )

    # 3️⃣ show assistant reply immediately
    assistant_msg = st.session_state.state["messages"][-1]
    with st.chat_message("assistant"):
        st.markdown(assistant_msg["content"])

    # 4️⃣ trigger full rerender so history includes the new turns
    st.rerun()
