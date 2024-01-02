from uuid import uuid4

from modules.rich_domain.module_1.core.domain.events import RichDomainModelCreated

from building_blocks.types import PK
from building_blocks.within_bounded_context.use_cases.command import Command, CommandHandler


class CreateRichDomainModel(Command):
    name: str


class CreateRichDomainModelHandler(CommandHandler):
    async def handle(self, command: CreateRichDomainModel) -> PK:
        pk = PK(uuid4())

        await self.event_bus.publish(
            RichDomainModelCreated(
                pk=pk,
                name=command.name,
            )
        )

        return pk
