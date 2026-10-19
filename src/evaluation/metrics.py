"""Metrics over benchmark records.

Record keys: task_id, category, success (agent's own tests passed), verified (hidden reference
tests passed, or None if the task has none), iterations, first_try (passed on iteration 1),
seconds, errors (list of failure texts).
"""
import json
import statistics
from collections import Counter
from pathlib import Path

from src.tools.debugger import classify_error, looks_hardcoded
from src.utils.config import ROOT


def _rate(n, d):
    return round(n / d, 4) if d else 0.0


def success_rate(results: list[dict]) -> float:
    return _rate(sum(r["success"] for r in results), len(results))


def hardcoded_ids(results: list[dict]) -> list[str]:
    """Tasks whose final code special-cases test inputs (detected from the saved code)."""
    return [r["task_id"] for r in results if r.get("final_code") and looks_hardcoded(r["final_code"])]


def clean_success_rate(results: list[dict]) -> float:
    """Success excluding solutions that pass by hard-coding test inputs."""
    bad = set(hardcoded_ids(results))
    return _rate(sum(r["success"] and r["task_id"] not in bad for r in results), len(results))


def verified_rate(results: list[dict]) -> float:
    """Share of tasks whose final code passes the hidden reference tests."""
    checked = [r for r in results if r.get("verified") is not None]
    return _rate(sum(r["verified"] for r in checked), len(checked))


def first_try_rate(results: list[dict]) -> float:
    return _rate(sum(r["first_try"] for r in results), len(results))


def self_fix_rate(results: list[dict]) -> float:
    """Of tasks that failed iteration 1, the share eventually fixed autonomously."""
    failed_first = [r for r in results if not r["first_try"]]
    return _rate(sum(r["success"] for r in failed_first), len(failed_first))


def wilson_interval(successes: int, n: int, z: float = 1.96) -> tuple[float, float]:
    """95% Wilson score interval for a proportion; honest about small samples (5/5 is not 100%)."""
    if n == 0:
        return (0.0, 1.0)
    p = successes / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5) / denom
    return (round(max(0.0, centre - half), 3), round(min(1.0, centre + half), 3))


def self_fix_counts(results: list[dict]) -> tuple[int, int]:
    failed_first = [r for r in results if not r["first_try"]]
    return sum(r["success"] for r in failed_first), len(failed_first)


def avg_iterations(results: list[dict]) -> dict:
    its = [r["iterations"] for r in results if r["success"]]
    if not its:
        return {"avg_iterations": 0, "median": 0, "max": 0, "min": 0}
    return {"avg_iterations": round(statistics.mean(its), 2), "median": statistics.median(its),
            "max": max(its), "min": min(its)}


def failure_analysis(results: list[dict]) -> dict:
    c = Counter(classify_error(r["errors"][-1]) for r in results if not r["success"] and r["errors"])
    return dict(c)


def by_category(results: list[dict]) -> dict:
    out = {}
    for cat in sorted({r["category"] for r in results}):
        rs = [r for r in results if r["category"] == cat]
        out[cat] = {"tasks": len(rs), "success_rate": success_rate(rs), "verified_rate": verified_rate(rs)}
    return out


def generate_report(results: list[dict], out_dir: Path | None = None) -> dict:
    report = {
        "total_tasks": len(results),
        "success_rate": success_rate(results),
        "clean_success_rate": clean_success_rate(results),
        "hardcoded_tasks": hardcoded_ids(results),
        "verified_rate": verified_rate(results),
        "first_try_rate": first_try_rate(results),
        "self_fix_rate": self_fix_rate(results),
        "self_fix_counts": list(self_fix_counts(results)),
        "self_fix_95ci": list(wilson_interval(*self_fix_counts(results))),
        "first_try_95ci": list(wilson_interval(sum(r["first_try"] for r in results), len(results))),
        "iterations": avg_iterations(results),
        "avg_seconds": round(statistics.mean(r["seconds"] for r in results), 1) if results else 0,
        "failure_modes": failure_analysis(results),
        "by_category": by_category(results),
    }
    if out_dir is not False:
        out_dir = out_dir or ROOT / "results" / "benchmarks"
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
        (out_dir / "raw_results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    return report
