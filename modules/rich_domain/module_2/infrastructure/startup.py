from fastapi import APIRouter

from modules.rich_domain.module_2.infrastructure.configuration import (
    event_bus as event_bus_config,
    message_bus as command_bus_config,
)
from modules.rich_domain.module_2.infrastructure.container import get_container


def get_routers() -> list[APIRouter]:
    from modules.rich_domain.module_2.api.some_endpoints import router

    return [router]


def startup() -> None:
    container = get_container()
    container.call_with_injection(
        container.get(event_bus_config.EventsSubscriptionsConfigurator).configure_subscriptions
    )
    container.call_with_injection(command_bus_config.configure_commands_mapping)
    container.call_with_injection(command_bus_config.configure_queries_mapping)
