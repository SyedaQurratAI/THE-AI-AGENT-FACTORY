from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

class ExtractedTask(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    source_jid: str
    original_text: str
    task_description: str
    assignee: str = "unknown"
    deadline: Optional[datetime] = None
    confidence_score: float = Field(ge=0.0, le=1.0)
    is_mention: bool = False
    status: str = "pending"
    created_at: datetime = Field(default_factory=datetime.utcnow)
