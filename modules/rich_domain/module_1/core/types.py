from typing import NewType

import injector

from modules.rich_domain.module_1.infrastructure.container import get_container
from modules.rich_domain.module_2.interface import Module as Module2Interface, get_module as get_module_2

Module2 = NewType("Module2", Module2Interface)


get_container().binder.bind(Module2, to=injector.CallableProvider(get_module_2), scope=injector.singleton)
