def get_code_gen_prompt(task: str) -> str:
    return (
        f"Task: {task}\n\nWrite a Python function named `solution` that solves this task.\n"
        "Provide ONLY the function in a ```python code block. No explanation. Standard library only."
    )


def get_solution_and_tests_prompt(task: str) -> str:
    """One request that yields both the solution and its tests (halves free-tier usage)."""
    return (
        f"Task: {task}\n\nWrite a Python function named `solution` that solves this task, then 3-5 pytest "
        "test functions (named test_*) for it, including edge cases.\n"
        "Reply with EXACTLY two ```python code blocks and no prose: first the function, then the tests. "
        "Cover every example and input format the task text mentions, exactly as written (do not assume extra "
        "whitespace or pre-cleaned input), and double-check each expected value by hand against the task text. "
        "The tests must not import the solution (it is in scope). Standard library only."
    )


def get_test_gen_prompt(code: str, task: str) -> str:
    return (
        f"Task: {task}\n\nFunction:\n```python\n{code}\n```\n\n"
        "Write 3-5 pytest test functions (named test_*) for `solution`, including edge cases. "
        "Do not import the solution; it is already in scope. Provide ONLY a ```python code block."
    )


def get_test_repair_prompt(task: str, code: str, tests: str, error: str) -> str:
    return (
        f"Task: {task}\n\nSolution:\n```python\n{code}\n```\n\nThese tests keep failing:\n```python\n{tests}\n```\n\n"
        f"Failure:\n{error[-1200:]}\n\n"
        "The solution may be right and a test's expected value may be WRONG (check arithmetic by hand against the "
        "task text). Write corrected pytest tests (3-5, named test_*) whose expectations follow the task exactly. "
        "Do not import the solution (it is already in scope). "
        "Provide ONLY a ```python code block."
    )


def get_fix_prompt(error: str, code: str, task: str = "") -> str:
    return (
        f"Task: {task}\n\nThis code failed:\n```python\n{code}\n```\n\nFailure:\n{error}\n\n"
        "Fix the code. Keep the function named `solution`. "
        "NEVER special-case or hard-code input values from the tests; implement the general behaviour the task "
        "describes, even if a test's expected value looks wrong. "
        "Provide ONLY the corrected function in a ```python code block."
    )
