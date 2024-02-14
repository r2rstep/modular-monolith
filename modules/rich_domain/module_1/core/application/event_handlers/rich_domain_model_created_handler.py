import injector

from modules.rich_domain.module_1.core.application.events import (
    RichDomainModelCreatedIntegrationEvent,
    RichDomainModelCreatedNotification,
)
from modules.rich_domain.module_1.core.domain.events import RichDomainModelCreated

from building_blocks.application.event_handlers import DomainEventHandler
from commons.applicaiton.generic_integration_event_publisher import build_generic_publish_integration_event_handler
from commons.database.db import InMemoryDb


class RichDomainModelCreatedHandler(DomainEventHandler[RichDomainModelCreated]):
    @injector.inject
    def __init__(self, db: InMemoryDb) -> None:
        self._db = db

    async def handle(self, event: RichDomainModelCreated) -> None:
        self._db.set(event.pk, event)


PublishRichDomainModelCreatedIntegrationEvent = build_generic_publish_integration_event_handler(
    RichDomainModelCreatedIntegrationEvent, RichDomainModelCreatedNotification
)
