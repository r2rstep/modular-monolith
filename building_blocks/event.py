from abc import abstractmethod
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class Event(BaseModel):
    occurred_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(frozen=True)

    @classmethod
    @abstractmethod
    def event_name(cls) -> str:
        pass
