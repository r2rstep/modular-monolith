import pytest

from building_blocks.within_bounded_context.application.event_handlers import DomainEventHandler
from building_blocks.within_bounded_context.domain.events import DomainEvent
from commons.event_bus.application.event_bus import EventBus


class SomethingHappened(DomainEvent):
    pass


something_happened_handled = False


class SomethingHappenedHandler(DomainEventHandler):
    async def handle(self, event: SomethingHappened) -> None:
        global something_happened_handled  # noqa: PLW0603
        something_happened_handled = True


class SomethingElseHappened(DomainEvent):
    pass


something_else_happened_handled = False


class SomethingElseHappenedHandler(DomainEventHandler):
    async def handle(self, event: SomethingElseHappened) -> None:
        global something_else_happened_handled  # noqa: PLW0603
        something_else_happened_handled = True


@pytest.mark.asyncio()
class TestEventBus:
    @pytest.fixture(autouse=True)
    def _init(self):
        self.event_bus = EventBus()

    async def test_publish_with_no_subscriptions_to_event(self) -> None:
        # given event bus with subscriptions
        self.event_bus.subscribe(SomethingHappened, SomethingHappenedHandler())

        # when publishing an event with no subscriptions
        await self.event_bus.publish(SomethingElseHappened())

        # then nothing happens
        assert not something_else_happened_handled

    async def test_publish_with_subscriptions_to_event(self) -> None:
        # given event bus with subscriptions
        self.event_bus.subscribe(SomethingHappened, SomethingHappenedHandler())

        # when publishing an event with subscriptions
        await self.event_bus.publish(SomethingHappened())

        # then event is handled
        assert something_happened_handled

    async def test_publish_with_multiple_subscriptions_to_event(self) -> None:
        # given event bus with subscriptions
        self.event_bus.subscribe(SomethingHappened, SomethingHappenedHandler())
        self.event_bus.subscribe(SomethingHappened, SomethingElseHappenedHandler())

        # when publishing an event with subscriptions
        await self.event_bus.publish(SomethingHappened())

        # then event is handled
        assert something_happened_handled
        assert something_else_happened_handled
