from modules.rich_domain.module_1.core.application.integration_events import RichDomainModelCreatedIntegrationEvent
from modules.rich_domain.module_1.core.domain.events import RichDomainModelCreated

from building_blocks.application.event_handlers import DomainEventHandler
from commons.applicaiton.generic_integration_event_publisher import build_generic_publish_integration_event_handler


class RichDomainModelCreatedHandler(DomainEventHandler[RichDomainModelCreated]):
    async def handle(self, event: RichDomainModelCreated) -> None:
        ...


PublishRichDomainModelCreatedIntegrationEvent = build_generic_publish_integration_event_handler(
    RichDomainModelCreatedIntegrationEvent, RichDomainModelCreated
)
