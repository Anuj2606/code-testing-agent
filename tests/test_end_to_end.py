"""Live end-to-end test against the real LLM. Skipped when no API key is configured."""
import pytest

from src.agent.code_agent import CodeGenerationAgent
from src.data.task_loader import load_coding_tasks
from src.evaluation.benchmarks import run_task
from src.utils import config

pytestmark = pytest.mark.skipif(not config.GEMINI_API_KEY, reason="no GEMINI_API_KEY")


def test_agent_solves_and_verifies_easy_task():
    task = next(t for t in load_coding_tasks() if t["id"] == "data_03")
    r = run_task(task, CodeGenerationAgent())
    assert r["success"] and r["verified"]
