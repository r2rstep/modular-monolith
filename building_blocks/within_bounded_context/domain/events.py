from abc import ABC
from datetime import datetime
from typing import TypeVar

from pydantic import BaseModel, ConfigDict, Field


# pydantic features are not really needed but for sake of better DevEx it's better to have all the events technicalities
# handled the same way
class DomainEvent(ABC, BaseModel):
    is_public: bool = False
    occurred_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(frozen=True)

    @property
    def name(self) -> str:
        return self.__class__.__name__


DomainEventType = TypeVar("DomainEventType", bound=DomainEvent)
