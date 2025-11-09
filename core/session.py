import streamlit as st
import uuid
from config.predefined_agents import PREDEFINED_AGENTS

def init_state():
    if "initialized" in st.session_state:
        return
    default_agents = [
        {"role": "Research Specialist", "goal": PREDEFINED_AGENTS["Research Specialist"]["goal"], "expertise": PREDEFINED_AGENTS["Research Specialist"]["expertise"]},
        {"role": "Technical Expert", "goal": PREDEFINED_AGENTS["Technical Expert"]["goal"], "expertise": PREDEFINED_AGENTS["Technical Expert"]["expertise"]},
        {"role": "Creative Writer", "goal": PREDEFINED_AGENTS["Creative Writer"]["goal"], "expertise": PREDEFINED_AGENTS["Creative Writer"]["expertise"]},
        {"role": "Quality Assurance", "goal": PREDEFINED_AGENTS["Quality Assurance"]["goal"], "expertise": PREDEFINED_AGENTS["Quality Assurance"]["expertise"]},
    ]
    st.session_state.agents_cfg = default_agents
    st.session_state.messages = []
    st.session_state.api_key = ""
    st.session_state.max_turns = 12
    st.session_state.current_task = ""
    st.session_state.file_content = {}
    st.session_state.session_id = str(uuid.uuid4())
    st.session_state.user_suggestions = ""
    st.session_state.export_ready = False
    st.session_state.saved_tasks = []
    st.session_state.initialized = True
