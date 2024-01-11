from building_blocks.within_bounded_context.application.command import Command
from modules.rich_domain.language import RichDomainModelName


class DoSomething(Command):
    name: RichDomainModelName
