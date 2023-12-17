from building_blocks.within_bounded_context.infrastructure.event_bus import init_event_bus


def start_modules() -> None:
    from modules.rich_domain import module_1

    event_bus = init_event_bus()

    module_1.startup.startup(event_bus)
