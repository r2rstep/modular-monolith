from abc import ABC
from dataclasses import dataclass

from building_blocks.within_bounded_context.application.command_bus import MessageBus


@dataclass
class ModuleInterface(ABC):
    command_bus: MessageBus
