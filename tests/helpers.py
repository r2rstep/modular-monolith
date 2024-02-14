from typing import Any

from building_blocks.event import Event


def excluding_occurred_at(event: Event) -> tuple[type[Event], dict[str, Any]]:
    return type(event), {k: v for k, v in dict(event).items() if k != "occurred_at"}
