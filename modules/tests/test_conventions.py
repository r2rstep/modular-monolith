import injector

from building_blocks.within_bounded_context.application.event_handlers import DomainEventHandler
from building_blocks.within_bounded_context.domain.events import DomainEvent, is_public_event
from commons.event_bus.application.event_bus import (
    EventBus,
    EventsSubscriptionsConfiguratorBase,
)
from commons.event_bus.event import Event
from commons.messagebox.infrastructure.messagebox import Inbox, Outbox
from commons.messagebox.types import PublicDomainEventsClsList
from commons.utils import get_all_subclasses

non_public_events = set()


class RestrictiveEventBus(EventBus):
    def subscribe(self, event_cls: type[Event], handler_cls: DomainEventHandler) -> None:
        if (
            event_cls.__module__ != handler_cls.__module__
            and issubclass(event_cls, DomainEvent)
            and not is_public_event(event_cls)
        ):
            non_public_events.add(event_cls)


class Container(injector.Module):
    def configure(self, binder: injector.Binder) -> None:
        binder.bind(EventBus, to=RestrictiveEventBus, scope=injector.singleton)
        binder.multibind(PublicDomainEventsClsList, to=[], scope=injector.singleton)

    @injector.singleton
    @injector.provider
    def outbox_provider(self) -> Outbox:
        return Outbox("test")

    @injector.singleton
    @injector.provider
    def inbox_provider(self) -> Inbox:
        return Inbox("test")


container = injector.Injector([Container()])


def test_module_cannot_subscribe_other_module_non_public_events():
    for configurator in get_all_subclasses(EventsSubscriptionsConfiguratorBase):
        container.call_with_injection(container.get(configurator).configure_subscriptions)

    assert non_public_events == set()
