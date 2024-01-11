from uuid import uuid4

import injector

from modules.rich_domain.module_1.core.domain.events import RichDomainModelCreated

from building_blocks.within_bounded_context.application.command import Command, CommandHandler
from commons.event_bus.application.event_bus import EventBus
from commons.types import PK
from modules.rich_domain.language import RichDomainModelName


class CreateRichDomainModel(Command):
    name: str


class CreateRichDomainModelHandler(CommandHandler[CreateRichDomainModel]):
    @injector.inject
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus

    async def handle(self, command: CreateRichDomainModel) -> PK:
        pk = PK(uuid4())

        await self.event_bus.publish(
            RichDomainModelCreated(
                pk=pk,
                name=RichDomainModelName(command.name),
            )
        )

        return pk
