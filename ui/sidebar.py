import streamlit as st
from config.predefined_agents import PREDEFINED_AGENTS

def render_sidebar():
    st.title("🛠️ Control Center")
    st.subheader("🔐 API Configuration")
    st.session_state.api_key = st.text_input("OpenAI API Key", type="password", value=st.session_state.api_key, help="Your key is used only for this session and never saved.")
    status = "✅ Connected" if st.session_state.api_key.startswith("sk-") else "❌ Not Connected"
    st.markdown(f"**Status:** {status}")
    st.divider()

    st.subheader("⚙️ Session Settings")
    st.session_state.max_turns = st.slider("Max Collaboration Rounds", 5, 25, st.session_state.max_turns)

    if st.session_state.messages:
        m = len(st.session_state.messages)
        a = len([x for x in st.session_state.messages if x.get("type") == "agent"])
        c1, c2 = st.columns(2)
        c1.metric("Messages", m)
        c2.metric("Agent Responses", a)
    st.divider()

    st.subheader("👥 Team Management")
    st.markdown("**Quick Team Setup:**")
    q1, q2 = st.columns(2)
    with q1:
        if st.button("🔬 Research Team", use_container_width=True):
            st.session_state.agents_cfg = [
                {"role": "Research Specialist", "goal": PREDEFINED_AGENTS["Research Specialist"]["goal"], "expertise": PREDEFINED_AGENTS["Research Specialist"]["expertise"]},
                {"role": "Data Analyst", "goal": PREDEFINED_AGENTS["Data Analyst"]["goal"], "expertise": PREDEFINED_AGENTS["Data Analyst"]["expertise"]},
                {"role": "Quality Assurance", "goal": PREDEFINED_AGENTS["Quality Assurance"]["goal"], "expertise": PREDEFINED_AGENTS["Quality Assurance"]["expertise"]},
            ]
            st.success("Research team configured")
    with q2:
        if st.button("💼 Business Team", use_container_width=True):
            st.session_state.agents_cfg = [
                {"role": "Marketing Strategist", "goal": PREDEFINED_AGENTS["Marketing Strategist"]["goal"], "expertise": PREDEFINED_AGENTS["Marketing Strategist"]["expertise"]},
                {"role": "Financial Advisor", "goal": PREDEFINED_AGENTS["Financial Advisor"]["goal"], "expertise": PREDEFINED_AGENTS["Financial Advisor"]["expertise"]},
                {"role": "Project Manager", "goal": PREDEFINED_AGENTS["Project Manager"]["goal"], "expertise": PREDEFINED_AGENTS["Project Manager"]["expertise"]},
            ]
            st.success("Business team configured")

    st.markdown("**Current Team:**")
    to_remove = None
    for i, agent in enumerate(st.session_state.agents_cfg):
        with st.expander(f"{PREDEFINED_AGENTS.get(agent['role'],{}).get('icon','🤖')} {agent['role']}", expanded=False):
            st.session_state.agents_cfg[i]['role'] = st.selectbox(
                "Select Role",
                options=list(PREDEFINED_AGENTS.keys()),
                index=list(PREDEFINED_AGENTS.keys()).index(agent['role']) if agent['role'] in PREDEFINED_AGENTS else 0,
                key=f"role_{i}"
            )
            sel = PREDEFINED_AGENTS[st.session_state.agents_cfg[i]['role']]
            st.session_state.agents_cfg[i]['goal'] = sel['goal']
            st.session_state.agents_cfg[i]['expertise'] = sel['expertise']
            st.markdown(f"**Expertise:** {sel['expertise']}")
            st.text_area("Goal", value=sel['goal'], height=100, key=f"goal_{i}", disabled=True)
            if st.button(f"Remove {agent['role']}", key=f"rm_{i}", type="secondary"):
                to_remove = i
    if to_remove is not None:
        st.session_state.agents_cfg.pop(to_remove)
        st.rerun()

    c1, c2 = st.columns(2)
    with c1:
        if st.button("➕ Add Agent", use_container_width=True):
            existing = [a['role'] for a in st.session_state.agents_cfg]
            choices = [r for r in PREDEFINED_AGENTS.keys() if r not in existing]
            if choices:
                r = choices[0]
                t = PREDEFINED_AGENTS[r]
                st.session_state.agents_cfg.append({"role": r, "goal": t["goal"], "expertise": t["expertise"]})
                st.rerun()
            else:
                st.warning("All agent types are in use")
    with c2:
        if st.button("🔄 Reset Team", use_container_width=True):
            st.session_state.agents_cfg = [
                {"role": "Research Specialist", "goal": PREDEFINED_AGENTS["Research Specialist"]["goal"], "expertise": PREDEFINED_AGENTS["Research Specialist"]["expertise"]},
                {"role": "Creative Writer", "goal": PREDEFINED_AGENTS["Creative Writer"]["goal"], "expertise": PREDEFINED_AGENTS["Creative Writer"]["expertise"]},
                {"role": "Quality Assurance", "goal": PREDEFINED_AGENTS["Quality Assurance"]["goal"], "expertise": PREDEFINED_AGENTS["Quality Assurance"]["expertise"]},
            ]
            st.rerun()

    st.divider()
    if st.button("🔄 New Session", use_container_width=True, type="secondary"):
        for k in ["messages", "file_content", "current_task", "user_suggestions"]:
            st.session_state[k] = [] if k == "messages" else ({} if k == "file_content" else "")
        import uuid
        st.session_state.session_id = str(uuid.uuid4())
        st.rerun()

    return {"status": status}
