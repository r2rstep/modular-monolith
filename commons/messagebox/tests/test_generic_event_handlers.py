import pytest

from building_blocks.application.command import Command
from building_blocks.application.notification_event import NotificationEvent
from building_blocks.domain.event import DomainEvent
from commons.messagebox.application.generic_event_handlers import (
    build_store_command_in_inbox_handler,
)
from commons.messagebox.infrastructure.messagebox import Inbox, MessageDTO, MessageTopic


class SomeEvent(DomainEvent):
    a: int
    b: str
    is_public: bool = True


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
        await handler.handle(NotificationEvent(domain_event=SomeEvent(a=1, b="test")))

        # then command is stored in inbox
        assert await inbox.get_next() == MessageDTO(MessageTopic("Command"), {})

    async def test_command_has_subset_of_events_attributes(self):
        # given inbox and command
        inbox = Inbox("test")

        # when handling an event
        handler_cls = build_store_command_in_inbox_handler(CompatibleCommand, SomeEvent)
        handler = handler_cls(inbox)
        await handler.handle(NotificationEvent(domain_event=SomeEvent(a=1, b="test")))

        # then command is stored in inbox
        assert await inbox.get_next() == MessageDTO(MessageTopic("CompatibleCommand"), {"a": 1})

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
            await handler.handle(NotificationEvent(domain_event=SomeEvent(a=1, b="test")))

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
            await handler.handle(NotificationEvent(domain_event=SomeEvent(a=1, b="test")))
