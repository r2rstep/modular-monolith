from modules.rich_domain.module_1.core.domain.events import RichDomainModelCreated
from modules.rich_domain.module_1.core.event_handlers.rich_domain_model_created_handler import (
    RichDomainModelCreatedHandler,
)

from building_blocks.within_bounded_context.infrastructure.event_bus import EventBus


def startup(event_bus: EventBus) -> None:
    event_bus.subscriptions[RichDomainModelCreated].append(RichDomainModelCreatedHandler)
