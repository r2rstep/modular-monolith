import pytest

from building_blocks.application.command import Command
from building_blocks.application.notification_event import NotificationEvent
from building_blocks.domain.event import DomainEvent
from commons.event_bus.application.event_bus import EventBus
from commons.message_bus.message_bus import MessageBus
from commons.messagebox.application.message_handlers import NotificationEventMessageHandler
from commons.messagebox.application.process_messagebox_commands import ProcessOutbox
from commons.messagebox.application.process_messagebox_handlers import (
    ProcessMessageboxHandler,
)
from commons.messagebox.infrastructure.messagebox import (
    Messagebox,
    MessageTopic,
    Outbox,
)


class DummyEvent(NotificationEvent, Command):
    param: int = 0
    should_fail: bool = False


class FakeBus(EventBus, MessageBus):
    def __init__(self) -> None:
        self.processed = []
        super().__init__()

    async def publish(self, event: NotificationEvent) -> None:
        if getattr(event, "should_fail", False):
            raise RuntimeError

        self.processed.append(event)

    async def execute(self, command: Command) -> None:
        if getattr(command, "should_fail", False):
            raise RuntimeError

        self.processed.append(command)

    async def execute_internal(self, command: Command) -> None:
        if getattr(command, "should_fail", False):
            raise RuntimeError

        self.processed.append(command)


@pytest.mark.asyncio()
class TestProcessOutboxHandler:
    @pytest.fixture()
    def fake_bus(self) -> FakeBus:
        return FakeBus()

    @pytest.fixture()
    def messagebox(self) -> Outbox:
        return Outbox("test")

    @pytest.fixture()
    def messagebox_handler(self, messagebox, fake_bus) -> ProcessMessageboxHandler:
        message_box_handler = ProcessMessageboxHandler(messagebox, {})
        message_box_handler.add_handler(
            MessageTopic(DummyEvent.event_name()), NotificationEventMessageHandler(DummyEvent, fake_bus)
        )
        return message_box_handler

    async def test_messagebox_empty(
        self,
        messagebox_handler: ProcessMessageboxHandler,
        fake_bus: FakeBus,
        messagebox: Messagebox,
    ):
        # given empty messagebox
        with messagebox.open():
            assert await messagebox.get_next_pending() is None

        # when processing the message box
        await messagebox_handler.handle(ProcessOutbox())

        # then nothing is published
        assert fake_bus.processed == []

    async def test_no_handler_for_message(
        self,
        messagebox_handler: ProcessMessageboxHandler,
        fake_bus: FakeBus,
        messagebox: Messagebox,
    ):
        # given messagebox with a message with name not in payload_cls_list
        class OtherEvent(DomainEvent):
            pass

        with messagebox.open():
            await messagebox.add(MessageTopic("OtherEvent"), OtherEvent().model_dump())

        # when processing the messagebox
        await messagebox_handler.handle(ProcessOutbox())

        # then the message is not processed
        assert fake_bus.processed == []

    async def test_call_handler(
        self,
        messagebox_handler: ProcessMessageboxHandler,
        fake_bus: FakeBus,
        messagebox: Messagebox,
    ):
        # given messagebox with a message
        event = DummyEvent(param=1)
        with messagebox.open():
            await messagebox.add(MessageTopic(event.event_name()), event.model_dump())

        # when processing the messagebox
        await messagebox_handler.handle(ProcessOutbox())

        # then the message is processed
        assert fake_bus.processed == [event]
