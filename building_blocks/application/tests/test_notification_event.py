from building_blocks.application.notification_event import NotificationEvent


class DummyEvent(NotificationEvent):
    a: int


def test_set_idempotency_id_when_not_given():
    notification_event = DummyEvent(a=1)
    assert notification_event.idempotency_id != ""

    notification_event = DummyEvent(a=1, idempotency_id="idempotency_id")
    assert notification_event.idempotency_id == "idempotency_id"
