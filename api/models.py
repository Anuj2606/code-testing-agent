from pydantic import BaseModel, Field


class TaskRequest(BaseModel):
    description: str = Field(min_length=3, max_length=2000)
    max_iterations: int = Field(default=5, ge=1, le=10)


class GenerateResponse(BaseModel):
    code: str
    tests: str


class TestRequest(BaseModel):
    code: str = Field(max_length=20000)
    tests: str = Field(max_length=20000)


class TestResponse(BaseModel):
    success: bool
    passed: int
    failed: int
    error: str


class AgentRunResponse(BaseModel):
    task_id: str
    task: str
    success: bool
    iterations: int
    final_code: str
    errors: list[str]
    conversation_history: list[dict]


class HistoryResponse(BaseModel):
    task_id: str
    task: str
    iterations: list[dict]


class StatusResponse(BaseModel):
    task_id: str
    status: str  # running | success | failed
    iterations: int
