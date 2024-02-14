from datetime import datetime
from typing import TypedDict

from pydantic import BaseModel, ConfigDict, Field


class EventDict(TypedDict):
    occurred_at: datetime


class Event(BaseModel):
    occurred_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(frozen=True)

    @classmethod
    def event_name(cls) -> str:
        return f"{cls.__bases__[0].__name__}__{cls.__name__}"
