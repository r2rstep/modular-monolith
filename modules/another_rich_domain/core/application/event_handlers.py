import injector

from modules.another_rich_domain.core.domain.events import SomeResourceCreated

from building_blocks.application.event_handlers import DomainEventHandler
from commons.database.db import InMemoryDb


class UpdateThisResource(DomainEventHandler[SomeResourceCreated]):
    @injector.inject
    def __init__(self, db: InMemoryDb) -> None:
        self._db = db

    async def handle(self, event: SomeResourceCreated) -> None:
        self._db.set(f"another {event.id}", event)
