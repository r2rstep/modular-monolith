from fastapi import APIRouter

from modules.rich_domain.module_1.infrastructure.configuration import (
    event_bus as event_bus_config,
    message_bus as message_bus_config,
)
from modules.rich_domain.module_1.infrastructure.container import get_container


def get_routers() -> list[APIRouter]:
    from modules.rich_domain.module_1.api.rich_domain_endpoints import router as rich_domain_resource_router

    router = APIRouter(prefix="/rich_domain_resources", tags=["rich_domain_resources"])
    router.include_router(rich_domain_resource_router)
    return [router]


def startup() -> None:
    container = get_container()
    container.call_with_injection(
        container.get(event_bus_config.EventsSubscriptionsConfigurator).configure_subscriptions
    )
    container.call_with_injection(message_bus_config.configure_commands_mapping)
    container.call_with_injection(message_bus_config.configure_queries_mapping)
