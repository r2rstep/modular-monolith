from building_blocks.application.notification_event import NotificationEvent
from building_blocks.domain.event import DomainEvent


class DummyDomainEvent(DomainEvent):
    a: int
    is_public: bool = True


def test_set_idempotency_id_when_not_given():
    notification_event = NotificationEvent(domain_event=DummyDomainEvent(a=1))
    assert notification_event.idempotency_id != ""

    notification_event = NotificationEvent(domain_event=DummyDomainEvent(a=1), idempotency_id="idempotency_id")
    assert notification_event.idempotency_id == "idempotency_id"


def test_event_name():
    assert (
        NotificationEvent[DummyDomainEvent].get_event_name(NotificationEvent[DummyDomainEvent])
        == "NotificationEvent__DummyDomainEvent"
    )

    notification_event = NotificationEvent[DummyDomainEvent](domain_event=DummyDomainEvent(a=1))
    assert notification_event.get_event_name(notification_event) == "NotificationEvent__DummyDomainEvent"
