from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class EmailMessage(BaseModel):
    id: str
    thread_id: str
    subject: str
    snippet: str
    sender: str
    received_at: Optional[datetime] = None
    body: Optional[str] = None
    labels: List[str] = []

    class Config:
        from_attributes = True
