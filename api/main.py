"""FastAPI server. Run: uvicorn api.main:app --port 8000"""
import threading
import uuid

from fastapi import FastAPI, HTTPException

from api import middleware
from api.models import (AgentRunResponse, GenerateResponse, HistoryResponse, StatusResponse,
                        TaskRequest, TestRequest, TestResponse)
from src.agent.code_agent import CodeGenerationAgent
from src.tools import code_generator
from src.tools.test_runner import run_tests

app = FastAPI(title="Code Generation Agent")
middleware.install(app)

# The agent keeps module-level state, so runs are serialised. Results are kept in memory.
app.state.agent_factory = CodeGenerationAgent
_run_lock = threading.Lock()
_runs: dict[str, dict] = {}


@app.post("/generate", response_model=GenerateResponse)
def generate(req: TaskRequest):
    code = code_generator.generate_code(req.description)
    return GenerateResponse(code=code, tests=code_generator.generate_tests(code, req.description))


@app.post("/test", response_model=TestResponse)
def test(req: TestRequest):
    r = run_tests(req.code, req.tests)
    return TestResponse(success=r["success"], passed=r["passed"], failed=r["failed"], error=r["error"])


@app.post("/agent-run", response_model=AgentRunResponse)
def agent_run(req: TaskRequest):
    task_id = str(uuid.uuid4())
    _runs[task_id] = {"task": req.description, "status": "running", "iterations": 0, "history": []}
    with _run_lock:
        result = app.state.agent_factory(max_iterations=req.max_iterations).run(req.description)
    _runs[task_id].update(status="success" if result["success"] else "failed",
                          iterations=result["iterations"], history=result["history"])
    return AgentRunResponse(task_id=task_id, task=req.description, success=result["success"],
                            iterations=result["iterations"], final_code=result["code"],
                            errors=[e[:1000] for e in result["errors"]],
                            conversation_history=result["history"])


def _get(task_id: str) -> dict:
    if task_id not in _runs:
        raise HTTPException(404, "unknown task_id")
    return _runs[task_id]


@app.get("/history/{task_id}", response_model=HistoryResponse)
def history(task_id: str):
    r = _get(task_id)
    return HistoryResponse(task_id=task_id, task=r["task"], iterations=r["history"])


@app.get("/status/{task_id}", response_model=StatusResponse)
def status(task_id: str):
    r = _get(task_id)
    return StatusResponse(task_id=task_id, status=r["status"], iterations=r["iterations"])


@app.get("/health")
def health():
    return {"ok": True}
