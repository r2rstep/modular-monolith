# TODO: usunąć
import pytest

from building_blocks.within_bounded_context.domain.events import (
    DomainEvent,
    DomainNotificationEvent,
)
from building_blocks.within_bounded_context.infrastructure.event_bus import EventBus
from building_blocks.within_bounded_context.infrastructure.messagebox import (
    Inbox,
    MessageBox,
    MessageDTO,
    MessageName,
)
from building_blocks.within_bounded_context.processing.process_inbox_command import ProcessInboxCommand
from building_blocks.within_bounded_context.processing.process_inbox_command_handler import ProcessInboxCommandHandler


@pytest.mark.asyncio()
class TestMessageBox:
    async def test_add_and_get_message(self):
        # given empty message_box
        message_box = MessageBox("test")

        # when adding a message
        await message_box.add(MessageName("test_message"), {"field_a": "value_a", "field_b": "value_b"})
        # and getting the message
        message = await message_box.get_next()

        # then message's name and payload are correct
        assert message == MessageDTO(MessageName("test_message"), {"field_a": "value_a", "field_b": "value_b"})
        # and message_box is empty
        assert await message_box.get_next() is None

    async def test_add_and_get_multiple_messages(self):
        # given empty message_box
        message_box = MessageBox("test")

        # when adding multiple messages
        messages_names = ["test_message_1", "test_message_2", "test_message_3"]
        for message_name in messages_names:
            await message_box.add(MessageName(message_name), {})

        # and getting all the messages
        messages = []
        while message := await message_box.get_next():
            messages.append(message)

        # then messages are returned in the same order as they were added
        assert [msg.name for msg in messages] == [MessageName(m_name) for m_name in messages_names]


@pytest.mark.asyncio()
class TestProcessInboxCommandHandler:
    class DummyNotification1(DomainNotificationEvent):
        field_a: str

    class DummyNotification2(DomainNotificationEvent):
        field_a: str

    class DummyEventBus(EventBus):
        def __init__(self):
            super().__init__()
            self.published_events = []

        def publish(self, event: DomainEvent):
            self.published_events.append(event)

    @pytest.fixture()
    def notifications_mapping(self):
        return {
            TestProcessInboxCommandHandler.DummyNotification1.name(): TestProcessInboxCommandHandler.DummyNotification1,
            TestProcessInboxCommandHandler.DummyNotification2.name(): TestProcessInboxCommandHandler.DummyNotification2,
        }

    @pytest.fixture()
    def event_bus(self):
        return TestProcessInboxCommandHandler.DummyEventBus()

    async def test_no_messages_in_inbox(self, event_bus, notifications_mapping):
        # given empty inbox
        inbox = Inbox("test")

        # when processing inbox
        await ProcessInboxCommandHandler(notifications_mapping, inbox, event_bus).handle(ProcessInboxCommand())

        # then no events are handled
        assert event_bus.published_events == []

    async def test_messages_in_inbox(self, event_bus, notifications_mapping):
        # given domain notification event added to the inbox
        inbox = Inbox("test")
        notification_1 = TestProcessInboxCommandHandler.DummyNotification1(field_a="value_a")
        await inbox.add(MessageName(notification_1.name()), dict(notification_1))
        notification_2 = TestProcessInboxCommandHandler.DummyNotification2(field_a="value_a")
        await inbox.add(MessageName(notification_2.name()), dict(notification_2))

        # when processing inbox
        await ProcessInboxCommandHandler(notifications_mapping, inbox, event_bus).handle(ProcessInboxCommand())

        # then the notification is published
        assert event_bus.published_events == [notification_1, notification_2]
        # and inbox is empty
        assert await inbox.get_next() is None

    async def test_exception_when_handling_message(self, event_bus, notifications_mapping):
        # given domain notification event added to the inbox
        inbox = Inbox("test")
        notification_1 = TestProcessInboxCommandHandler.DummyNotification1(field_a="value_a")
        await inbox.add(MessageName(notification_1.name()), dict(notification_1))
        notification_2 = TestProcessInboxCommandHandler.DummyNotification2(field_a="value_a")
        await inbox.add(MessageName(notification_2.name()), dict(notification_2))

        # when processing inbox and exception is raised when handling the first message

        # then 2nd message is still handled
