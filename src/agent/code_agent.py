"""ReAct-style agent: THINK -> ACT -> OBSERVE -> DECIDE until tests pass or iterations run out."""
import time

from src.agent import state_manager as sm
from src.tools import code_generator, debugger, test_runner
from src.utils.config import MAX_ITERATIONS
from src.utils.logger import get_logger


class CodeGenerationAgent:
    def __init__(self, max_iterations: int = MAX_ITERATIONS, generator=code_generator):
        self.max_iterations = max_iterations
        self.gen = generator  # injectable for offline tests
        self.history: list[dict] = []
        self.log = get_logger()

    def run(self, task_description: str) -> dict:
        state = sm.initialize_state(task_description)
        self.history = []
        self.api_error = False
        for i in range(1, self.max_iterations + 1):
            state.iteration = i
            plan = self.think()
            result = self.act(plan)
            outcome = self.observe(result)
            self.log.info("iter=%d action=%s outcome=%s", i, plan["action"], outcome)
            if outcome == "SUCCESS":
                state.phase = "SUCCESS"
                return self._result(True)
            if result.get("api_error"):
                self.api_error = True
                break
        state.phase = "FAILED"
        return self._result(False)

    def think(self) -> dict:
        s = sm.get_current_state()
        if not s.code:
            return {"action": "generate"}
        h = self.history
        if len(h) >= 2 and debugger.same_failure(h[-2]["result"], h[-1]["result"]):
            # The same test failed twice despite a fix: the test's expectation is suspect.
            return {"action": "repair_tests", "error": s.last_result.get("error", "")}
        return {"action": "fix", "error": debugger.generate_fix_prompt(s.last_result.get("error", ""), s.code)}

    def act(self, plan: dict) -> dict:
        s = sm.get_current_state()
        try:
            if plan["action"] == "generate":
                if hasattr(self.gen, "generate_solution_and_tests"):  # one request instead of two
                    s.code, s.tests = self._with_retry(self.gen.generate_solution_and_tests, s.task)
                else:
                    s.code = self._with_retry(self.gen.generate_code, s.task)
                    s.tests = self._with_retry(self.gen.generate_tests, s.code, s.task)  # fixed once, from the first draft
            elif plan["action"] == "repair_tests":
                # Discard any test-gaming hack: go back to the latest non-hard-coded version of the code.
                honest = [c for c in s.versions if not debugger.looks_hardcoded(c)]
                s.code = honest[-1] if honest else s.code
                if hasattr(self.gen, "repair_tests"):
                    s.tests = self._with_retry(self.gen.repair_tests, s.task, s.code, s.tests, plan["error"])
                else:
                    s.tests = self._with_retry(self.gen.generate_tests, s.code, s.task)
            else:
                s.code = self._with_retry(self.gen.generate_code, s.task, plan["error"], s.code)
        except Exception as e:  # API still failing after retries: not a code failure, so don't burn iterations
            return {"success": False, "api_error": True, "error": f"{type(e).__name__}: {e}"}
        s.versions.append(s.code)
        return test_runner.run_tests(s.code, s.tests)

    def _with_retry(self, fn, *args, attempts: int = 3, base_delay: float = 2.0):
        for n in range(attempts):
            try:
                return fn(*args)
            except Exception as e:
                msg = str(e)
                # The router already rotates models and waits out rate limits; QuotaExhausted means all are spent.
                if (n == attempts - 1 or type(e).__name__ == "QuotaExhausted" or "404" in msg
                        or "API_KEY" in msg.upper() or "PerDay" in msg):
                    raise  # permanent errors (bad model / key / daily quota) won't fix themselves
                self.log.warning("API error (%s), retry %d/%d", type(e).__name__, n + 1, attempts - 1)
                time.sleep(base_delay * 2**n)

    def observe(self, result: dict) -> str:
        s = sm.get_current_state()
        if result.get("success") and debugger.looks_hardcoded(s.code):
            # Passing by special-casing test inputs is not a pass.
            # It dodged the tests that failed before, so carry them over (lets same_failure spot the loop).
            prev = self.history[-1]["result"].get("failed_tests", []) if self.history else []
            result = {**result, "success": False, "hardcoded": True, "failed_tests": prev,
                      "error": "Hard-coded test inputs detected in solution(); implement the general behaviour."}
        sm.update_state("EVALUATE", result)
        self.history.append({"iteration": s.iteration, "code": s.code, "result": result})
        if result.get("success"):
            return "SUCCESS"
        s.errors.append(result.get("error", ""))
        return "CONTINUE"

    def get_conversation_history(self) -> list[dict]:
        return self.history

    def _result(self, success: bool) -> dict:
        s = sm.get_current_state()
        return {"success": success, "iterations": s.iteration, "code": s.code,
                "errors": s.errors, "history": self.history, "api_error": self.api_error,
                "hardcoded_attempts": sum(1 for h in self.history if h["result"].get("hardcoded"))}
