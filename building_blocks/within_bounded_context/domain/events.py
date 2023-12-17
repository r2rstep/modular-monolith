from abc import ABC, abstractmethod
from datetime import datetime
from typing import TypeVar

from pydantic import BaseModel, ConfigDict, Field


# pydantic features are not really needed but for sake of better DevEx it's better to have all the events technicalities
# handled the same way
class DomainEvent(ABC, BaseModel):
    occurred_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(frozen=True)

    @classmethod
    def name(cls) -> str:
        return cls.__name__


DomainEventType = TypeVar("DomainEventType", bound=DomainEvent)


class DomainEventHandler(ABC):
    @abstractmethod
    async def handle(self, event: DomainEvent) -> None:
        ...
