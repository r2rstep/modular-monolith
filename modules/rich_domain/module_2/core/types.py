from typing import NewType

import injector

from modules.rich_domain.module_1.interface import Module as Module1Interface, get_module as get_module_1
from modules.rich_domain.module_2.infrastructure.container import get_container

Module1 = NewType("Module1", Module1Interface)


get_container().binder.bind(Module1, to=injector.CallableProvider(get_module_1), scope=injector.singleton)
