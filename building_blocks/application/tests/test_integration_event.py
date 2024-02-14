import pytest

from building_blocks.application.integration_event import IntegrationEvent
from building_blocks.application.notification_event import NotificationEvent


class DummyIntegrationEvent(IntegrationEvent):
    a: int


class DummyNotificationEvent(NotificationEvent):
    a: int


def test_integration_event_can_only_be_created_from_notification_event():
    with pytest.raises(
        RuntimeError, match="IntegrationEvent instances must be created via from_notification_event method."
    ):
        DummyIntegrationEvent(a=1, idempotency_id="idempotency_id")

    assert DummyIntegrationEvent.from_notification_event(DummyNotificationEvent(a=1))
