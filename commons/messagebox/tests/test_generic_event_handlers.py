import pytest

from building_blocks.application.command import Command
from building_blocks.application.notification_event import NotificationEvent
from building_blocks.domain.event import DomainEvent
from commons.messagebox.application.generic_event_handlers import (
    build_store_command_in_inbox_handler,
    build_store_notification_in_outbox_handler,
)
from commons.messagebox.infrastructure.messagebox import Inbox, MessageDTO, MessageTopic, Outbox


class SomeEvent(NotificationEvent):
    a: int
    b: str


class CompatibleCommand(Command):
    a: int


class CommandWithDifferentAnnotations(Command):
    a: str


class CommandWithDifferentAttributes(Command):
    c: int


@pytest.mark.asyncio()
class TestGenericStoreCommandBasedOnEventInInbox:
    async def test_command_with_no_attributes(self):
        # given inbox and command
        inbox = Inbox("test")

        # when handling an event
        handler_cls = build_store_command_in_inbox_handler(Command, SomeEvent)
        handler = handler_cls(inbox)
        await handler.handle(SomeEvent(a=1, b="test"))

        # then command is stored in inbox
        assert await inbox.get_next() == MessageDTO(MessageTopic("Command__Command"), {})

    async def test_command_has_subset_of_events_attributes(self):
        # given inbox and command
        inbox = Inbox("test")

        # when handling an event
        handler_cls = build_store_command_in_inbox_handler(CompatibleCommand, SomeEvent)
        handler = handler_cls(inbox)
        await handler.handle(SomeEvent(a=1, b="test"))

        # then command is stored in inbox
        assert await inbox.get_next() == MessageDTO(MessageTopic("Command__CompatibleCommand"), {"a": 1})

    async def test_command_has_different_annotations_than_event(self):
        # given inbox and command
        inbox = Inbox("test")

        # when handling an event
        handler_cls = build_store_command_in_inbox_handler(CommandWithDifferentAnnotations, SomeEvent)
        handler = handler_cls(inbox)
        with pytest.raises(
            ValueError,
            match=(
                "Command and event attributes have different annotations."
                f" Command: {CommandWithDifferentAnnotations}, event: {SomeEvent}"
            ),
        ):
            await handler.handle(SomeEvent(a=1, b="test"))

    async def test_command_has_different_attributes_than_event(self):
        # given inbox and command
        inbox = Inbox("test")

        # when handling an event
        handler_cls = build_store_command_in_inbox_handler(CommandWithDifferentAttributes, SomeEvent)
        handler = handler_cls(inbox)
        with pytest.raises(
            ValueError,
            match=(
                "Command attributes are not a subset of event attributes."
                f" Command: {CommandWithDifferentAttributes}, event: {SomeEvent}"
            ),
        ):
            await handler.handle(SomeEvent(a=1, b="test"))


class DummyEvent(DomainEvent):
    a: int
    b: str


@pytest.mark.asyncio()
async def test_generic_store_integration_event_in_inbox():
    # given inbox and event
    outbox = Outbox("test")

    # when handling an event
    domain_event = DummyEvent(a=1, b="test")
    handler = build_store_notification_in_outbox_handler(SomeEvent, DummyEvent)
    await handler(outbox).handle(domain_event)

    # then command is stored in inbox
    result = await outbox.get_next()
    result_payload_without_randoms = {
        k: v for k, v in result.payload.items() if k not in ["idempotency_id", "occurred_at"]
    }
    assert (result.topic, result_payload_without_randoms) == (
        MessageTopic("NotificationEvent__SomeEvent"),
        {"a": 1, "b": "test"},
    )
