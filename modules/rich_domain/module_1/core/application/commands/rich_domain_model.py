from uuid import uuid4

from modules.rich_domain.module_1.core.domain.events import RichDomainModelCreated

from building_blocks.types import PK
from building_blocks.within_bounded_context.application.command import Command, CommandHandler
from modules.rich_domain.language import RichDomainModelName


class CreateRichDomainModel(Command):
    name: str


class CreateRichDomainModelHandler(CommandHandler):
    async def handle(self, command: CreateRichDomainModel) -> PK:
        pk = PK(uuid4())

        await self.event_bus.publish(
            RichDomainModelCreated(
                pk=pk,
                name=RichDomainModelName(command.name),
            )
        )

        return pk