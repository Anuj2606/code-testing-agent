from src.data.test_datasets import TASKS


def load_coding_tasks(num_tasks: int | None = None, category: str | None = None) -> list[dict]:
    tasks = [t for t in TASKS if category is None or t["category"] == category]
    return tasks[:num_tasks] if num_tasks else tasks


def load_custom_tasks(items: list[tuple[str, str]]) -> list[dict]:
    """Ad-hoc tasks without reference tests: [(id, description), ...]."""
    return [{"id": i, "category": "custom", "difficulty": "n/a", "description": d, "reference_tests": ""}
            for i, d in items]
