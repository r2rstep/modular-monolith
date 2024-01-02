from fastapi import APIRouter

from building_blocks.within_bounded_context.infrastructure.command_bus import CommandToHandlerMapping
from building_blocks.within_bounded_context.infrastructure.event_bus import EventBus
from infrastructure.container.global_container import global_container
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
    event_bus_config.configure_subscriptions(global_container.get(EventBus))
    command_bus_config.configure_commands_mapping(container.get(CommandToHandlerMapping), container)
