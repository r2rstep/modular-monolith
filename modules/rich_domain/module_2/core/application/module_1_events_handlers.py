from building_blocks.within_bounded_context.application.command import Command, CommandHandler
from modules.rich_domain.language import RichDomainModelName


class DoSomething(Command):
    name: RichDomainModelName


class CreateSomething(CommandHandler[DoSomething]):
    async def handle(self, command: DoSomething) -> None:
        print(f"Creating something with name {command.name}")  # noqa: T201
