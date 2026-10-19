"""Benchmark plots, saved to results/plots/."""
from collections import Counter
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from src.evaluation.metrics import by_category, failure_analysis  # noqa: E402
from src.utils.config import ROOT  # noqa: E402


def generate_plots(results: list[dict], out_dir: Path | None = None) -> list[Path]:
    out = out_dir or ROOT / "results" / "plots"
    out.mkdir(parents=True, exist_ok=True)
    paths = []

    cats = by_category(results)
    fig, ax = plt.subplots(figsize=(7, 4))
    x = range(len(cats))
    ax.bar([i - 0.2 for i in x], [c["success_rate"] for c in cats.values()], 0.4, label="agent tests pass")
    ax.bar([i + 0.2 for i in x], [c["verified_rate"] for c in cats.values()], 0.4, label="hidden tests pass")
    ax.set_xticks(list(x), list(cats), rotation=20, ha="right")
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("rate")
    ax.set_title("Success by task category")
    ax.legend()
    paths.append(_save(fig, out / "success_rate_by_task.png"))

    its = Counter(r["iterations"] for r in results if r["success"])
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(list(its), list(its.values()))
    ax.set_xlabel("iterations to success")
    ax.set_ylabel("tasks")
    ax.set_title("Iterations distribution")
    paths.append(_save(fig, out / "iterations_distribution.png"))

    fails = failure_analysis(results) or {"none": 0}
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(list(fails), list(fails.values()))
    ax.set_title("Failure modes")
    paths.append(_save(fig, out / "error_type_breakdown.png"))

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar([r["task_id"] for r in results], [r["seconds"] for r in results])
    ax.tick_params(axis="x", rotation=75)
    ax.set_ylabel("seconds")
    ax.set_title("Time per task")
    paths.append(_save(fig, out / "time_per_task.png"))
    return paths


def _save(fig, path: Path) -> Path:
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)
    return path
