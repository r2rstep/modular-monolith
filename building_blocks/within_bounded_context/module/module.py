from abc import ABC
from dataclasses import dataclass

from building_blocks.within_bounded_context.infrastructure.command_bus import CommandBus


@dataclass
class ModuleInterface(ABC):
    command_bus: CommandBus
