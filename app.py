import streamlit as st
from core.session import init_state
from ui.layout import render_header, render_messages, render_footer
from ui.sidebar import render_sidebar
from core.processor import process_uploaded_files
from core.agents import Employee, Manager
from core.export import build_export_package
from datetime import datetime
import uuid
import time

def main():
    st.set_page_config(page_title="Krew Pro - AI Agent Organization", page_icon="🤖", layout="wide", initial_sidebar_state="expanded")
    init_state()

    render_header()

    with st.sidebar:
        sidebar_out = render_sidebar()

    st.subheader("📁 Document Upload & Processing")
    col_u, col_m = st.columns([2, 1])
    with col_u:
        files = st.file_uploader("Upload documents", accept_multiple_files=True, type=["pdf", "docx", "txt", "csv"])
        if files:
            with st.spinner("Processing files..."):
                st.session_state.file_content = process_uploaded_files(files)
            st.success(f"Processed {len(st.session_state.file_content)} file(s)")
            for name, content in st.session_state.file_content.items():
                with st.expander(f"📄 {name} ({len(content)} chars)"):
                    st.text_area("Preview", content[:500] + ("..." if len(content) > 500 else ""), height=120, disabled=True)

    with col_m:
        if st.session_state.file_content:
            st.metric("Files Loaded", len(st.session_state.file_content))
            total_chars = sum(len(x) for x in st.session_state.file_content.values())
            st.metric("Total Characters", f"{total_chars:,}")
            if st.button("🗑️ Clear Files", use_container_width=True):
                st.session_state.file_content = {}
                st.rerun()

    st.divider()
    st.subheader("🎯 Mission Control")
    col_t, col_e = st.columns([3, 1])
    with col_t:
        task = st.text_area("Describe your task", value=st.session_state.current_task, height=120, placeholder="Example: Analyze uploaded data and create a comprehensive strategy...")
        st.session_state.current_task = task
    with col_e:
        examples = ["Market Analysis Report", "Technical Documentation", "Creative Content Strategy", "Data Analysis & Insights", "Business Process Optimization"]
        st.markdown("**Quick Examples:**")
        for ex in examples:
            if st.button(ex, use_container_width=True, key=f"ex_{ex}"):
                st.session_state.current_task = f"Create a comprehensive {ex.lower()} using provided info."
                st.rerun()

    with st.expander("🔧 Advanced Options", expanded=False):
        st.session_state.user_suggestions = st.text_area("Additional context or requirements", value=st.session_state.user_suggestions, height=80)
        c1, c2, c3 = st.columns(3)
        with c1:
            creativity = st.select_slider("Creativity", options=["Conservative", "Balanced", "Innovative"], value="Balanced")
        with c2:
            detail = st.select_slider("Detail", options=["Summary", "Standard", "Comprehensive"], value="Standard")
        with c3:
            priority = st.select_slider("Priority", options=["Standard", "High", "Critical"], value="Standard")
        pref = f"\nQuality Preferences: Creativity={creativity}, Detail={detail}, Priority={priority}"
        if st.session_state.user_suggestions and "Quality Preferences:" not in st.session_state.user_suggestions:
            st.session_state.user_suggestions += pref

    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        execute = st.button(
            "🚀 Deploy Agents",
            use_container_width=True,
            type="primary",
            disabled=(not st.session_state.api_key.startswith("sk-")) or (not st.session_state.current_task.strip())
        )
    with c2:
        if st.button("💾 Save Task", use_container_width=True, disabled=not st.session_state.current_task.strip()):
            st.session_state.saved_tasks.append({"task": st.session_state.current_task, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"), "id": str(uuid.uuid4())})
            st.success("Task saved")
    with c3:
        if st.button("📋 Load Task", use_container_width=True):
            if st.session_state.saved_tasks:
                with st.popover("Select saved task"):
                    for i, t in enumerate(reversed(st.session_state.saved_tasks)):
                        if st.button(f"{t['timestamp']}: {t['task'][:48]}...", key=f"load_{i}"):
                            st.session_state.current_task = t['task']
                            st.rerun()
            else:
                st.info("No saved tasks")

    if not st.session_state.api_key.startswith("sk-"):
        st.warning("Enter your OpenAI API key in the sidebar.")
    elif not st.session_state.current_task.strip():
        st.info("Describe your task to begin.")
    elif len(st.session_state.agents_cfg) == 0:
        st.warning("Add at least one agent in the sidebar.")

    st.divider()

    if execute:
        if not st.session_state.api_key.startswith("sk-") or not st.session_state.current_task.strip() or not st.session_state.agents_cfg:
            st.stop()

        st.session_state.messages = []
        files_blob = ""
        if st.session_state.file_content:
            files_blob = "\n\n".join([f"=== {n} ===\n{c}" for n, c in st.session_state.file_content.items()])

        employees = []
        for a in st.session_state.agents_cfg:
            employees.append(Employee(role=a['role'], goal=a['goal'], expertise=a.get('expertise', ''), api_key=st.session_state.api_key))

        manager = Manager(employees=employees, api_key=st.session_state.api_key, max_turns=st.session_state.max_turns)

        progress = st.progress(0.0)
        status = st.empty()
        steps = len(employees) * st.session_state.max_turns + 6
        count = 0

        for out in manager.delegate_task(st.session_state.current_task, file_content=files_blob, user_suggestions=st.session_state.user_suggestions):
            st.session_state.messages.append(out)
            count += 1
            progress.progress(min(count / steps, 1.0))
            if out.get("type") == "final_result":
                status.text("Completed")
                progress.progress(1.0)
                st.session_state.export_ready = True
                break
            else:
                status.text(f"Processing: {out.get('sender', 'System')}")
            time.sleep(0.2)
        progress.empty()
        status.empty()
        st.rerun()

    if st.session_state.messages:
        render_messages()

    st.divider()
    if st.session_state.messages and any(m.get("type") == "final_result" for m in st.session_state.messages):
        st.subheader("📤 Export")
        data = build_export_package(
            session_id=st.session_state.session_id,
            messages=st.session_state.messages,
            agents_cfg=st.session_state.agents_cfg,
            max_turns=st.session_state.max_turns
        )
        st.download_button("📦 Download Package", data=data, file_name=f"krew_session_{st.session_state.session_id[:8]}.zip", mime="application/zip", use_container_width=True)

    render_footer()

if __name__ == "__main__":
    main()
