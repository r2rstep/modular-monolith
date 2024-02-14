import importlib
import inspect
from pathlib import Path

from importlinter.cli import lint_imports
import pytest

from building_blocks.application.command import Command
from building_blocks.application.integration_event import IntegrationEvent
from building_blocks.application.notification_event import NotificationEvent
from building_blocks.application.query import Query
from commons.message_bus.message_bus import MessageBus


@pytest.fixture(scope="session")
def existing_modules():
    modules = list(Path(__file__).parent.parent.glob("modules/**/core"))
    modules = [str(module)[str(module).find("/modules/") :] for module in modules]
    return [module.lstrip("/").rstrip("/core").replace("/", ".") for module in modules]


def test_modules_can_expose_only_commands_and_queries_and_public_events_and_message_bus(existing_modules):
    violations = {}
    checks = {
        "is_command": lambda attr_type: issubclass(attr_type, Command),
        "is_query": lambda attr_type: issubclass(attr_type, Query),
        "is_message_bus": lambda attr_type: issubclass(attr_type, MessageBus),
        "is_notification_event": lambda attr_type: issubclass(attr_type, NotificationEvent),
        "is_integration_event": lambda attr_type: issubclass(attr_type, IntegrationEvent),
    }

    for module_path in existing_modules:
        module_cls = importlib.import_module(module_path + ".interface").Module
        for field, value in filter(lambda attr: not attr[0].startswith("_"), inspect.getmembers(module_cls)):
            if not any(
                check(value if inspect.isclass(value) else value.__class__) for check_name, check in checks.items()
            ):
                violations.update({f"{module_cls}": field})

        assert not violations


def test_import_linter(pyproject_toml_path):
    assert lint_imports(str(pyproject_toml_path)) == 0
