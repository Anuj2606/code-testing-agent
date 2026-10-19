"""Streamlit UI. Run: streamlit run ui/streamlit_app.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import streamlit as st  # noqa: E402

from src.agent.code_agent import CodeGenerationAgent  # noqa: E402

st.set_page_config(page_title="Code Generation Agent", layout="wide")
st.title("Code Generation Agent")
st.caption("Generates code, writes tests, runs them in a sandbox, and fixes failures on its own.")

task = st.text_area("Coding task", placeholder="Write solution(items): sort dicts by their 'age' key ...", height=100)
max_iter = st.sidebar.slider("Max iterations", 1, 10, 5)

if st.button("Run Agent", type="primary", disabled=len(task.strip()) < 3):
    with st.spinner("Agent working..."):
        result = CodeGenerationAgent(max_iterations=max_iter).run(task.strip())

    (st.success if result["success"] else st.error)(
        f"{'Tests passed' if result['success'] else 'Gave up'} after {result['iterations']} iteration(s)")

    left, right = st.columns(2)
    with left:
        st.subheader("Final code")
        st.code(result["code"], language="python")
    with right:
        st.subheader("Iterations")
        for h in result["history"]:
            ok = h["result"].get("success")
            with st.expander(f"Iteration {h['iteration']}: {'PASS' if ok else 'FAIL'}", expanded=not ok):
                st.code(h["code"], language="python")
                if not ok:
                    st.text(h["result"].get("error", "")[-1500:])
