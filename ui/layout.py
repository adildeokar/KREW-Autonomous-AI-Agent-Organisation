import streamlit as st
from config.predefined_agents import PREDEFINED_AGENTS
from datetime import datetime

CSS = """
<style>
    .main-header {background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 10px; color: white; text-align: center; margin-bottom: 2rem;}
</style>
"""

def render_header():
    st.markdown(CSS, unsafe_allow_html=True)
    st.markdown('<div class="main-header"><h1>🤖 Krew - The AI Agent Organization</h1><p>Specialized agents collaborate to solve complex tasks</p><p>Made by AMP Squad - MIT ADTU, SIH 2025</p></div>', unsafe_allow_html=True)

def render_messages():
    st.subheader("💬 Agent Collaboration")
    total = len(st.session_state.messages)
    agent_msgs = len([m for m in st.session_state.messages if m.get("type") == "agent"])
    finals = len([m for m in st.session_state.messages if m.get("type") == "final_result"])
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Total Messages", total)
    with c2: st.metric("Agent Responses", agent_msgs)
    with c3: st.metric("Completed Tasks", finals)
    with c4:
        if st.session_state.messages:
            first_ts = st.session_state.messages[0].get("timestamp")
            st.metric("Session Time", "—" if not first_ts else "Active")

    box = st.container()
    with box:
        for i, m in enumerate(st.session_state.messages):
            t = m.get("type", "message")
            sender = m.get("sender", "Unknown")
            content = m.get("message", "")
            ts = m.get("timestamp", "")
            if t == "final_result":
                st.markdown(f"### 🎉 Final Result from {sender}  \n<small>{ts}</small>", unsafe_allow_html=True)
                st.markdown(content)
                c1, c2, c3 = st.columns(3)
                with c1:
                    if st.button("👍 Great Result", key=f"like_{i}"):
                        st.success("Feedback recorded")
                with c2:
                    if st.button("🔄 Request Refinement", key=f"ref_{i}"):
                        r = st.text_input("What would you like improved?", key=f"in_{i}")
                        if r:
                            st.session_state.user_suggestions += f"\nRefinement: {r}"
                with c3:
                    if st.button("📤 Share Result", key=f"sh_{i}"):
                        st.code(content)
            elif t == "manager":
                with st.chat_message("assistant", avatar="👨‍💼"):
                    st.markdown(f"**{sender}** *{ts}*")
                    st.markdown(content)
            elif t == "agent":
                icon = PREDEFINED_AGENTS.get(sender, {}).get("icon", "🤖")
                with st.chat_message("assistant", avatar=icon):
                    st.markdown(f"**{sender}** *{ts}*")
                    st.markdown(content)
            elif t == "thinking":
                with st.chat_message("assistant"):
                    st.markdown(f"*{content}*")
            elif t == "completion":
                st.success(content)
            elif t == "timeout":
                st.warning(content)
            else:
                with st.chat_message("assistant"):
                    st.markdown(f"**{sender}** *{ts}*")
                    st.markdown(content)
    if st.session_state.messages:
        st.markdown('<div id="bottom"></div>', unsafe_allow_html=True)
        st.markdown("<script>document.getElementById('bottom').scrollIntoView({behavior:'smooth'});</script>", unsafe_allow_html=True)

def render_footer():
    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("**🤖 Krew - The AI Agent Organization**")
        st.caption("SIH 2025 - MIT ADTU")
        st.caption("Built By AMP Squad")
    with c2:
        if st.session_state.messages:
            st.markdown(f"**Session ID:** `{st.session_state.session_id[:8]}...`")
        st.caption("Adil Deokar | Monika Jadhav")
        st.caption("Pranav Bulbule | Soham Bagul")
        st.caption("Abha Deshmukh | Sarthak Chakurkar")
    with c3:
        st.markdown(f"**Status:** {'🟢 Active' if st.session_state.api_key.startswith('sk-') else '🔴 Inactive'}")
        st.caption(f"Agents: {len(st.session_state.agents_cfg)}")
