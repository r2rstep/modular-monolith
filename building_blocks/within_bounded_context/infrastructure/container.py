from typing import Any, Optional

from building_blocks.within_bounded_context.infrastructure.event_bus import EventBus


class ModuleContainer:
    __instance = None

    def __new__(cls, *_: Any, **__: dict[str, Any]) -> "ModuleContainer":  # noqa: ANN401
        if ModuleContainer.__instance is None:
            ModuleContainer.__instance = object.__new__(cls)
        return ModuleContainer.__instance

    def __init__(self, event_bus: Optional[EventBus] = None):
        if hasattr(self, "event_bus"):
            return

        self.event_bus = event_bus
