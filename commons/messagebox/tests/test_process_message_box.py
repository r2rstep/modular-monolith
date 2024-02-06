from typing import Callable, Union

from pydantic import BaseModel
import pytest

from building_blocks.within_bounded_context.application.command import Command
from building_blocks.within_bounded_context.application.notification_event import NotificationEvent
from building_blocks.within_bounded_context.domain.events import DomainEvent
from commons.event_bus.application.event_bus import EventBus
from commons.message_bus.message_bus import MessageBus
from commons.messagebox.application.process_messagebox_commands import ProcessInbox, ProcessOutbox
from commons.messagebox.application.process_messagebox_handlers import (
    ProcessInboxCommandsHandler,
    ProcessMessageboxHandler,
    ProcessOutboxDomainEventsHandler,
)
from commons.messagebox.infrastructure.messagebox import Inbox, Messagebox, MessageDTO, MessageName, Outbox


class DummyEventOrCommand(DomainEvent, Command):
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
    def fake_bus(self):
        return FakeBus()

    @pytest.fixture(params=[ProcessOutboxDomainEventsHandler, ProcessInboxCommandsHandler])
    def handler_cls(self, request):
        return request.param

    @pytest.fixture()
    def messagebox(self, handler_cls):
        return Outbox("test") if handler_cls == ProcessOutboxDomainEventsHandler else Inbox("test")

    @pytest.fixture()
    def messagebox_handler(self, fake_bus, messagebox, handler_cls):
        return handler_cls(messagebox, fake_bus, [DummyEventOrCommand])

    @pytest.fixture()
    def process_command(self, handler_cls):
        return ProcessOutbox() if handler_cls == ProcessOutboxDomainEventsHandler else ProcessInbox()

    @pytest.fixture()
    def build_message(self, handler_cls) -> Callable[[Union[DomainEvent, Command]], tuple[MessageName, BaseModel]]:
        def build_notification_payload(event: DomainEvent) -> tuple[MessageName, BaseModel]:
            return MessageName(event.name), NotificationEvent(domain_event=event)

        def build_command_payload(command: Command) -> tuple[MessageName, BaseModel]:
            return MessageName(command.name), command

        return build_notification_payload if handler_cls == ProcessOutboxDomainEventsHandler else build_command_payload

    async def test_messagebox_empty(
        self,
        messagebox_handler: ProcessMessageboxHandler,
        process_command: Command,
        fake_bus: FakeBus,
        messagebox: Messagebox,
    ):
        # given empty messagebox
        assert await messagebox.get_next() is None

        # when processing the message box
        await messagebox_handler.handle(process_command)

        # then nothing is published
        assert fake_bus.processed == []

    async def test_already_processed_message_is_not_processed_again(
        self,
        messagebox_handler: ProcessMessageboxHandler,
        process_command: Command,
        fake_bus: FakeBus,
        messagebox: Messagebox,
        build_message: Callable[[BaseModel], tuple[MessageName, BaseModel]],
    ):
        # given messagebox with a processed message
        name, payload = build_message(DummyEventOrCommand())
        await messagebox.add(name, payload.model_dump())
        await messagebox_handler.handle(process_command)

        assert fake_bus.processed == [payload]
        fake_bus.processed = []

        # when processing the messagebox again
        await messagebox_handler.handle(process_command)

        # then message is not processed again
        assert fake_bus.processed == []

    async def test_message_is_added_back_to_messagebox_if_processing_fails(
        self,
        messagebox_handler: ProcessMessageboxHandler,
        process_command: Command,
        fake_bus: FakeBus,
        messagebox: Messagebox,
        build_message: Callable[[BaseModel], tuple[MessageName, BaseModel]],
    ):
        # given messagebox with multiple messages with some for which handling should fail
        message_name_and_payload = [
            build_message(DummyEventOrCommand(param=1, should_fail=True)),
            build_message(DummyEventOrCommand(param=2, should_fail=False)),
            build_message(DummyEventOrCommand(param=3, should_fail=True)),
        ]
        for name, payload in message_name_and_payload:
            await messagebox.add(name, payload.model_dump())

        # when processing the messagebox
        await messagebox_handler.handle(process_command)

        # then the failed messages are added back to the messagebox
        messagebox_messages = []
        while message := await messagebox.get_next():
            messagebox_messages.append(message)
        assert messagebox_messages == [
            MessageDTO(MessageName("DummyEventOrCommand"), message_name_and_payload[0][1].model_dump()),
            MessageDTO(MessageName("DummyEventOrCommand"), message_name_and_payload[2][1].model_dump()),
        ]
        # and the successful messages are published
        assert fake_bus.processed == [message_name_and_payload[1][1]]

    async def test_payload_cls_list_does_not_include_message_name(
        self,
        messagebox_handler: ProcessMessageboxHandler,
        process_command: Command,
        fake_bus: FakeBus,
        messagebox: Messagebox,
    ):
        # given messagebox with a message with name not in payload_cls_list
        class OtherEventOrCommand(DomainEvent, Command):
            pass

        await messagebox.add(MessageName("OtherEventOrCommand"), OtherEventOrCommand().model_dump())

        # when processing the messagebox
        await messagebox_handler.handle(process_command)

        # then the message is not processed
        assert fake_bus.processed == []
