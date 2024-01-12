from typing import cast

from building_blocks.within_bounded_context.domain.events import DomainEvent, is_public_event
from commons.utils import ClassProtocol, get_all_subclasses


def get_module_name_from_file_path(module_path: str) -> str:
    module_path = module_path[module_path.find("modules") :]
    module_path = module_path.lstrip("modules").lstrip("/")
    return module_path.replace("/", ".")


def get_python_module_from_file_path(module_path: str) -> str:
    module_path = module_path[module_path.find("modules") :]
    return module_path.replace("/", ".")


def get_module_all_public_events_classes(module_path: str) -> list[type[DomainEvent]]:
    return [
        event_cls
        for event_cls in get_all_subclasses(cast(type[ClassProtocol[DomainEvent]], DomainEvent))
        if is_public_event(event_cls) and event_cls.__module__.startswith(module_path)
    ]
