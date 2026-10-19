"""Benchmark runner: agent per task, then hidden-test verification of the final code."""
import json
import time
from pathlib import Path

from src.agent.code_agent import CodeGenerationAgent
from src.data.task_loader import load_coding_tasks
from src.evaluation.metrics import generate_report
from src.tools.code_executor import execute_code
from src.utils.config import ROOT
from src.utils.logger import get_logger

log = get_logger("benchmark")


def run_task(task: dict, agent: CodeGenerationAgent) -> dict:
    t0 = time.time()
    out = agent.run(task["description"])
    verified = None
    if task.get("reference_tests") and out["code"]:
        verified = execute_code(out["code"], task["reference_tests"])["success"]
    first = out["history"][0]["result"].get("success", False) if out["history"] else False
    return {"task_id": task["id"], "category": task["category"], "difficulty": task["difficulty"],
            "success": out["success"], "verified": verified, "iterations": out["iterations"],
            "first_try": bool(first), "seconds": round(time.time() - t0, 1),
            "final_code": out["code"], "errors": out["errors"], "api_error": out.get("api_error", False),
            "hardcoded_attempts": out.get("hardcoded_attempts", 0)}


def run_batch(batch_size: int, agent=None, results_file: Path | None = None) -> tuple[list[dict], dict]:
    """Run the next `batch_size` not-yet-done tasks and merge into the saved results.

    Tasks cut short by an API error (quota, outage) are not recorded: they say nothing about the
    agent, and the batch stops so the task is retried next time.
    """
    results_file = results_file or ROOT / "results" / "benchmarks" / "raw_results.json"
    done = json.loads(results_file.read_text()) if results_file.exists() else []
    done_ids = {r["task_id"] for r in done}
    agent = agent or CodeGenerationAgent()
    ran = 0
    for task in load_coding_tasks():
        if task["id"] in done_ids:
            continue
        if ran >= batch_size:
            break
        r = run_task(task, agent)
        if r["api_error"]:
            log.warning("API error on %s; stopping batch (task not recorded)", task["id"])
            break
        done.append(r)
        ran += 1
        log.info("%s success=%s verified=%s iters=%d (%.1fs)", task["id"], r["success"], r["verified"],
                 r["iterations"], r["seconds"])
        results_file.parent.mkdir(parents=True, exist_ok=True)
        results_file.write_text(json.dumps(done, indent=2), encoding="utf-8")  # save after every task
    return done, generate_report(done, results_file.parent) if done else {}


def run_benchmark(agent=None, num_tasks: int | None = None, category: str | None = None,
                  save: bool = True, delay: float = 0.0) -> tuple[list[dict], dict]:
    agent = agent or CodeGenerationAgent()
    tasks = load_coding_tasks(num_tasks, category)
    results = []
    for i, task in enumerate(tasks, 1):
        r = run_task(task, agent)
        results.append(r)
        log.info("[%d/%d] %s success=%s verified=%s iters=%d (%.1fs)", i, len(tasks), task["id"],
                 r["success"], r["verified"], r["iterations"], r["seconds"])
        time.sleep(delay)
    report = generate_report(results, None if save else False)
    return results, report
