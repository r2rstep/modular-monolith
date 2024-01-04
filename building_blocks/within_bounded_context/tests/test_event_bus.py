import pytest

from building_blocks.within_bounded_context.application.event_handlers import DomainEventHandler
from building_blocks.within_bounded_context.domain.events import DomainEvent
from building_blocks.within_bounded_context.infrastructure.event_bus import EventBus
from building_blocks.within_bounded_context.infrastructure.messagebox import Outbox, MessageDTO, MessageName


class SomethingHappened(DomainEvent):
    pass


something_happened_handled = False


class SomethingHappenedHandler(DomainEventHandler):
    async def handle(self, event: SomethingHappened) -> None:
        global something_happened_handled
        something_happened_handled = True


class SomethingElseHappened(DomainEvent):
    pass


something_else_happened_handled = False


class SomethingElseHappenedHandler(DomainEventHandler):
    async def handle(self, event: SomethingElseHappened) -> None:
        global something_else_happened_handled
        something_else_happened_handled = True


@pytest.mark.asyncio
class TestEventBus:
    @pytest.fixture(autouse=True)
    def init(self):
        self.outbox = Outbox("test")
        self.event_bus = EventBus(self.outbox)

    async def test_publish_with_no_subscriptions_to_event(self) -> None:
        # given event bus with subscriptions
        self.event_bus.subscribe(SomethingHappened, SomethingHappenedHandler)

        # when publishing an event with no subscriptions
        await self.event_bus.publish(SomethingElseHappened())

        # then nothing happens
        global something_else_happened_handled

        assert not something_else_happened_handled

    async def test_publish_with_subscriptions_to_event(self) -> None:
        # given event bus with subscriptions
        self.event_bus.subscribe(SomethingHappened, SomethingHappenedHandler)

        # when publishing an event with subscriptions
        await self.event_bus.publish(SomethingHappened())

        # then event is handled
        global something_happened_handled

        assert something_happened_handled

    async def test_publish_with_multiple_subscriptions_to_event(self) -> None:
        # given event bus with subscriptions
        self.event_bus.subscribe(SomethingHappened, SomethingHappenedHandler)
        self.event_bus.subscribe(SomethingHappened, SomethingElseHappenedHandler)

        # when publishing an event with subscriptions
        await self.event_bus.publish(SomethingHappened())

        # then event is handled
        global something_happened_handled
        global something_else_happened_handled

        assert something_happened_handled
        assert something_else_happened_handled
    
    @pytest.mark.parametrize('is_public', [True, False])
    async def test_store_public_event_to_outbox(self, is_public) -> None:
        # given event bus without subscriptions

        # when publishing an event
        event = SomethingHappened(is_public=is_public)
        await self.event_bus.publish(event)

        # then the event is stored in the outbox if it's public
        if is_public:
            assert await self.outbox.get_next() == MessageDTO(MessageName("SomethingHappened"), dict(event))
        else:
            assert await self.outbox.get_next() is None
