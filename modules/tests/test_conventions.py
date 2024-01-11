import injector

from building_blocks.within_bounded_context.application.event_handlers import DomainEventHandler
from building_blocks.within_bounded_context.domain.events import DomainEvent, is_public_event
from infrastructure.event_bus import EventBus, EventHandlingMediatorBase, EventsSubscriptionsConfiguratorBase


def get_all_subclasses(cls: type) -> list[type]:
    return cls.__subclasses__() + [g for s in cls.__subclasses__() for g in get_all_subclasses(s)]


non_public_events = set()


class RestrictiveEventBus(EventBus):
    def subscribe(
        self, event_cls: type[DomainEvent], handler_cls: type[DomainEventHandler], _: EventHandlingMediatorBase
    ) -> None:
        if event_cls.__module__ != handler_cls.__module__ and not is_public_event(event_cls):
            non_public_events.add(event_cls)


class DummyEventMediator(EventHandlingMediatorBase):
    async def handle(self, event: DomainEvent, handler_cls: type[DomainEventHandler]) -> None:
        ...


class Container(injector.Module):
    def configure(self, binder: injector.Binder) -> None:
        binder.bind(EventBus, to=RestrictiveEventBus, scope=injector.singleton)

    @injector.provider
    def event_mediator_provider(self) -> EventHandlingMediatorBase:
        return DummyEventMediator()


container = injector.Injector([Container()])


def test_module_cannot_subscribe_other_module_non_public_events():
    for configurator in get_all_subclasses(EventsSubscriptionsConfiguratorBase):
        container.call_with_injection(configurator().configure_subscriptions)

    assert non_public_events == set()
