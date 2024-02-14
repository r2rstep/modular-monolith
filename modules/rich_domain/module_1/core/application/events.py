from building_blocks.application.integration_event import IntegrationEvent
from building_blocks.application.notification_event import NotificationEvent
from commons.types import PK
from modules.rich_domain.language import RichDomainModelName


class RichDomainModelCreatedNotification(NotificationEvent):
    pk: PK
    name: RichDomainModelName


class RichDomainModelCreatedIntegrationEvent(IntegrationEvent):
    name: RichDomainModelName
