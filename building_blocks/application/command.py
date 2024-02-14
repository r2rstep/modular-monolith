from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict

from commons.types import PK, NoneOr


class Command(ABC, BaseModel):
    model_config = ConfigDict(frozen=True)

    @classmethod
    def command_name(cls) -> str:
        return f"Command__{cls.__name__}"


CommandType = TypeVar("CommandType", bound=Command)


class CommandHandler(ABC, Generic[CommandType]):
    @abstractmethod
    async def handle(self, command: CommandType) -> NoneOr[PK]:
        ...
