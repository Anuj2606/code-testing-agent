from dataclasses import dataclass, field


@dataclass
class AgentState:
    task: str = ""
    phase: str = "INIT"  # INIT, GENERATE, TEST, EVALUATE, DEBUG, SUCCESS, FAILED
    iteration: int = 0
    code: str = ""
    tests: str = ""
    last_result: dict = field(default_factory=dict)
    errors: list = field(default_factory=list)
    versions: list = field(default_factory=list)  # memory of every code version


_state = AgentState()


def initialize_state(task: str) -> AgentState:
    global _state
    _state = AgentState(task=task, phase="GENERATE")
    return _state


def update_state(action: str, result: dict) -> AgentState:
    _state.phase = action
    _state.last_result = result
    return _state


def get_current_state() -> AgentState:
    return _state


def reset_state() -> AgentState:
    global _state
    _state = AgentState()
    return _state
