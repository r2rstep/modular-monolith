from fastapi import APIRouter

from modules.rich_domain.module_1.infrastructure.configuration import (
    command_bus as command_bus_config,
    event_bus as event_bus_config,
)
from modules.rich_domain.module_1.infrastructure.container import container


def get_routers() -> list[APIRouter]:
    from modules.rich_domain.module_1.api.rich_domain_endpoints import router as rich_domain_resource_router

    router = APIRouter(prefix="/rich_domain_resources", tags=["rich_domain_resources"])
    router.include_router(rich_domain_resource_router)
    return [router]


def startup() -> None:
    container.call_with_injection(event_bus_config.EventsSubscriptionsConfigurator().configure_subscriptions)
    container.call_with_injection(command_bus_config.configure_commands_mapping)
