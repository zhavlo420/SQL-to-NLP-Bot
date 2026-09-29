from pydantic import BaseModel, Field
from typing import Any, Optional

class ChatRequest(BaseModel):
    question: str = Field(min_length=2, max_length=2000)
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    answer: str
    sql: Optional[str] = None
    rows: list[dict[str, Any]] = []
    columns: list[str] = []
    trace: list[dict[str, str]] = []
    assumptions: list[str] = []
