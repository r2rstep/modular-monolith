from fastapi import APIRouter

import modules.crud.infrastructure.configuration.message_bus as message_bus_config
from modules.crud.infrastructure.container import get_container


def get_routers() -> list[APIRouter]:
    from modules.crud.api.crud_data_endpoints import router

    return [router]


def startup() -> None:
    container = get_container()
    container.call_with_injection(message_bus_config.configure_commands_mapping)
    container.call_with_injection(message_bus_config.configure_queries_mapping)
