from fastapi import APIRouter

from modules.rich_domain.module_2.infrastructure.configuration import event_bus as event_bus_config
from modules.rich_domain.module_2.infrastructure.container import container


def get_routers() -> list[APIRouter]:
    return []


def startup() -> None:
    container.call_with_injection(event_bus_config.EventsSubscriptionsConfigurator().configure_subscriptions)
