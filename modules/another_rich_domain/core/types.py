from typing import NewType

import injector

from modules.another_rich_domain.infrastructure.container import get_container
from modules.rich_domain.module_1.interface import Module as Module1Interface, get_module as get_module_1

Module1 = NewType("Module1", Module1Interface)


get_container().binder.bind(Module1, to=injector.CallableProvider(get_module_1), scope=injector.singleton)
