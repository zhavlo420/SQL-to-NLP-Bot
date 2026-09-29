from typing import TypedDict, Any

class AgentState(TypedDict, total=False):
    question: str
    intent: dict[str, Any]
    schema: list[dict[str, Any]]
    plan: list[str]
    sql: str
    review: dict[str, Any]
    result: dict[str, Any]
    analysis: dict[str, Any]
    answer: str
    trace: list[dict[str, str]]
    assumptions: list[str]
    retry_count: int
