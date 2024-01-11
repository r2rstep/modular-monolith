from abc import ABC, abstractmethod
from typing import Generic, TypeVar

import injector
from pydantic import BaseModel, ConfigDict

from commons.event_bus.application.event_bus import EventBus
from commons.types import PK, NoneOr


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
