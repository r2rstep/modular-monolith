from typing import Generic, TypeVar

from pydantic import PrivateAttr

from building_blocks.application.command import Command as CommandBase
from building_blocks.application.query import Query as QueryBase
from building_blocks.dto import DTO
from commons.message_bus.message_bus import MessageBus
from commons.types import PK, NoneOr
from modules.another_rich_domain.infrastructure.container import get_container

ResultType = TypeVar("ResultType", bound=DTO)


class Query(QueryBase, Generic[ResultType]):
    _message_bus: MessageBus = PrivateAttr(default_factory=lambda: get_container().get(MessageBus))

    async def handle(self) -> ResultType:
        result: ResultType = await self._message_bus.query(self)
        return result


class Command(CommandBase):
    _message_bus: MessageBus = PrivateAttr(default_factory=lambda: get_container().get(MessageBus))

    async def handle(self) -> NoneOr[PK]:
        return await self._message_bus.execute(self)
