from abc import ABC, abstractmethod

from pydantic import BaseModel, ConfigDict

from building_blocks.types import PK, NoneOr


class Command(ABC, BaseModel):
    model_config = ConfigDict(frozen=True)


class CommandHandler:
    @abstractmethod
    def handle(self, command: Command) -> NoneOr[PK]:
        ...
