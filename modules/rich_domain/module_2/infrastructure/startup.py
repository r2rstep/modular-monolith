from fastapi import APIRouter

from modules.rich_domain.module_2.infrastructure.configuration import (
    command_bus as command_bus_config,
    event_bus as event_bus_config,
)
from modules.rich_domain.module_2.infrastructure.container import container


def get_routers() -> list[APIRouter]:
    return []


def startup() -> None:
    container.call_with_injection(
        container.get(event_bus_config.EventsSubscriptionsConfigurator).configure_subscriptions
    )
    container.call_with_injection(command_bus_config.configure_commands_mapping)
