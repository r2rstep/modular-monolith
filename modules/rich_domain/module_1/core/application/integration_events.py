from building_blocks.application.integration_event import IntegrationEvent
from modules.rich_domain.language import RichDomainModelName


class RichDomainModelCreatedIntegrationEvent(IntegrationEvent):
    name: RichDomainModelName
