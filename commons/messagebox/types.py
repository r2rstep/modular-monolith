from building_blocks.within_bounded_context.application.command import Command
from building_blocks.within_bounded_context.domain.events import DomainEvent

PublicDomainEventsClsList = list[type[DomainEvent]]
CommandsList = list[type[Command]]
