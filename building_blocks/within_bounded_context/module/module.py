from abc import ABC
from dataclasses import dataclass

from building_blocks.within_bounded_context.application.message_bus import MessageBus


@dataclass
class ModuleInterface(ABC):
    message_bus: MessageBus
