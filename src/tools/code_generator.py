"""Code and test generation via the LLM router."""
from src.prompts.generation_prompts import (get_code_gen_prompt, get_fix_prompt,
                                            get_solution_and_tests_prompt, get_test_gen_prompt,
                                            get_test_repair_prompt)
from src.tools.llm import complete
from src.utils.helpers import extract_code_block, extract_code_blocks, sanitize_tests


def generate_solution_and_tests(task: str) -> tuple[str, str]:
    """Single request returning (code, tests). Falls back to a second request if the reply has one block."""
    blocks = extract_code_blocks(complete(get_solution_and_tests_prompt(task), "generate"))
    if len(blocks) >= 2:
        return blocks[0], sanitize_tests(blocks[1])
    code = blocks[0] if blocks else ""
    return code, generate_tests(code, task)


def generate_code(task: str, error_context: str = "", previous_code: str = "") -> str:
    if error_context:
        return extract_code_block(complete(get_fix_prompt(error_context, previous_code, task), "fix"))
    return extract_code_block(complete(get_code_gen_prompt(task), "generate"))


def repair_tests(task: str, code: str, tests: str, error: str) -> str:
    return sanitize_tests(extract_code_block(complete(get_test_repair_prompt(task, code, tests, error), "tests")))


def generate_tests(code: str, task: str) -> str:
    return sanitize_tests(extract_code_block(complete(get_test_gen_prompt(code, task), "tests")))
