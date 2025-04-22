from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import datetime

class Participant(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str


class Blacklist(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    participant_id: int
    blocked_id: int


class Draw(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    giver: str
    receiver: str