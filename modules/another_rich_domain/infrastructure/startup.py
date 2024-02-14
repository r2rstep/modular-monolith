from modules.another_rich_domain.infrastructure.configuration.event_bus import EventsSubscriptionsConfigurator
from modules.another_rich_domain.infrastructure.configuration.message_bus import configure_commands_mapping
from modules.another_rich_domain.infrastructure.container import get_container


def startup() -> None:
    container = get_container()
    container.call_with_injection(configure_commands_mapping)
    container.call_with_injection(container.get(EventsSubscriptionsConfigurator).configure_subscriptions)
