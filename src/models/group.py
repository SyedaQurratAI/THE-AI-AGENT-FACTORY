from datetime import datetime
from pydantic import BaseModel, Field

class MonitoredGroup(BaseModel):
    jid: str
    name: str
    active: bool = True
    added_at: datetime = Field(default_factory=datetime.utcnow)
