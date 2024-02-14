import injector

from building_blocks.application.command import Command, CommandHandler
from commons.database.db import InMemoryDb
from modules.rich_domain.language import RichDomainModelName


class DoSomething(Command):
    name: RichDomainModelName


class CreateSomething(CommandHandler[DoSomething]):
    @injector.inject
    def __init__(self, db: InMemoryDb) -> None:
        self._db = db

    async def handle(self, command: DoSomething) -> None:
        self._db.set(f"command {command.name}", command)
