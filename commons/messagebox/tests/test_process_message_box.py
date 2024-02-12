from pydantic import BaseModel
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
    MessageDTO,
    MessageTopic,
    Outbox,
)


class DummyEvent(DomainEvent, Command):
    param: int = 0
    should_fail: bool = False
    is_public: bool = True


class FakeBus(EventBus, MessageBus):
    def __init__(self) -> None:
        self.processed = []
        super().__init__()

    async def publish(self, event: NotificationEvent) -> None:
        if getattr(event.domain_event, "should_fail", False):
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
        message_box_handler = ProcessMessageboxHandler(messagebox)
        message_box_handler.add_handler(
            MessageTopic(DummyEvent.event_name()), NotificationEventMessageHandler(DummyEvent, fake_bus)
        )
        return message_box_handler

    def build_message(self, event: DomainEvent) -> tuple[MessageTopic, BaseModel]:
        return MessageTopic(event.event_name()), NotificationEvent(domain_event=event)

    async def test_messagebox_empty(
        self,
        messagebox_handler: ProcessMessageboxHandler,
        fake_bus: FakeBus,
        messagebox: Messagebox,
    ):
        # given empty messagebox
        assert await messagebox.get_next() is None

        # when processing the message box
        await messagebox_handler.handle(ProcessOutbox())

        # then nothing is published
        assert fake_bus.processed == []

    async def test_already_processed_message_is_not_processed_again(
        self,
        messagebox_handler: ProcessMessageboxHandler,
        fake_bus: FakeBus,
        messagebox: Messagebox,
    ):
        # given messagebox with a processed message
        name, payload = self.build_message(DummyEvent())
        await messagebox.add(name, payload.model_dump())
        await messagebox_handler.handle(ProcessOutbox())

        assert fake_bus.processed == [payload]
        fake_bus.processed = []

        # when processing the messagebox again
        await messagebox_handler.handle(ProcessOutbox())

        # then message is not processed again
        assert fake_bus.processed == []

    async def test_message_is_added_back_to_messagebox_if_processing_fails(
        self,
        messagebox_handler: ProcessMessageboxHandler,
        fake_bus: FakeBus,
        messagebox: Messagebox,
    ):
        # given messagebox with multiple messages with some for which handling should fail
        message_name_and_payload = [
            self.build_message(DummyEvent(param=1, should_fail=True)),
            self.build_message(DummyEvent(param=2, should_fail=False)),
            self.build_message(DummyEvent(param=3, should_fail=True)),
        ]
        for name, payload in message_name_and_payload:
            await messagebox.add(name, payload.model_dump())

        # when processing the messagebox
        await messagebox_handler.handle(ProcessOutbox())

        # then the failed messages are added back to the messagebox
        messagebox_messages = []
        while message := await messagebox.get_next():
            messagebox_messages.append(message)
        assert messagebox_messages == [
            MessageDTO(MessageTopic(DummyEvent.event_name()), message_name_and_payload[0][1].model_dump()),
            MessageDTO(MessageTopic(DummyEvent.event_name()), message_name_and_payload[2][1].model_dump()),
        ]
        # and the successful messages are published
        assert fake_bus.processed == [message_name_and_payload[1][1]]

    async def test_no_handler_for_message(
        self,
        messagebox_handler: ProcessMessageboxHandler,
        fake_bus: FakeBus,
        messagebox: Messagebox,
    ):
        # given messagebox with a message with name not in payload_cls_list
        class OtherEvent(DomainEvent):
            pass

        await messagebox.add(MessageTopic("OtherEvent"), OtherEvent().model_dump())

        # when processing the messagebox
        await messagebox_handler.handle(ProcessOutbox())

        # then the message is not processed
        assert fake_bus.processed == []
