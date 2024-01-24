from abc import ABC, abstractmethod
from typing import Generic, TypeVar

import injector
from pydantic import BaseModel, ConfigDict

from building_blocks.types import PK, NoneOr
from infrastructure.event_bus import EventBus


class Command(ABC, BaseModel):
    model_config = ConfigDict(frozen=True)


CommandType = TypeVar("CommandType", bound=Command)


class CommandHandler(ABC, Generic[CommandType]):
    @injector.inject
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    @abstractmethod
    async def handle(self, command: CommandType) -> NoneOr[PK]:
        ...
