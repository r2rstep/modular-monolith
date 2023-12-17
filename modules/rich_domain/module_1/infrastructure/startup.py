from fastapi import APIRouter

from building_blocks.within_bounded_context.infrastructure.event_bus import EventBus
from modules.rich_domain.module_1.infrastructure.configuration import event_bus as event_bus_config
from modules.rich_domain.module_1.infrastructure.container import Container


def get_router() -> APIRouter:
    from modules.rich_domain.module_1.api.rich_domain_endpoints import router as rich_domain_resource_router

    router = APIRouter()
    router.include_router(rich_domain_resource_router)
    return router


def startup(event_bus: EventBus) -> None:
    Container(event_bus)
    event_bus_config.startup(event_bus)
