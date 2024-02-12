from typing import TypedDict

from modules.another_rich_domain.core.domain.events import SomeResourceCreated

from building_blocks.application.bounded_context_translator import BoundedContextTranslator
from modules.another_rich_domain.language import SomeModelId


class RichDomainModelCreatedIntegrationEventTranslator(BoundedContextTranslator):
    class RichDomainModelCreatedIntegrationEvent(TypedDict):
        name: str

    def translate(self, integration_event_payload: RichDomainModelCreatedIntegrationEvent) -> SomeResourceCreated:  # type: ignore[override]
        return SomeResourceCreated(id=SomeModelId(integration_event_payload["name"]))
