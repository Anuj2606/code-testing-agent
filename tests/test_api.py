"""API tests with a fake generator injected, so no LLM calls are made."""
from fastapi.testclient import TestClient

from api.main import app
from src.agent.code_agent import CodeGenerationAgent
from tests.test_agent_loop import FakeGen

app.state.agent_factory = lambda max_iterations=5: CodeGenerationAgent(max_iterations, generator=FakeGen())
client = TestClient(app)


def test_test_endpoint():
    r = client.post("/test", json={"code": "def solution(x):\n    return x\n",
                                   "tests": "def test_a():\n    assert solution(1) == 1\n"})
    assert r.status_code == 200 and r.json()["success"] and r.json()["passed"] == 1


def test_test_endpoint_rejects_unsafe_code():
    r = client.post("/test", json={"code": "import os\n", "tests": "def test_a():\n    pass\n"})
    assert not r.json()["success"] and "Restricted" in r.json()["error"]


def test_agent_run_history_status():
    r = client.post("/agent-run", json={"description": "sort a list"})
    body = r.json()
    assert r.status_code == 200 and body["success"] and body["iterations"] == 2
    tid = body["task_id"]
    assert client.get(f"/status/{tid}").json() == {"task_id": tid, "status": "success", "iterations": 2}
    assert len(client.get(f"/history/{tid}").json()["iterations"]) == 2


def test_validation_and_404():
    assert client.post("/agent-run", json={"description": "x"}).status_code == 422
    assert client.get("/status/nope").status_code == 404
