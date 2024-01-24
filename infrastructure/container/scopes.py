import contextvars
from typing import Any

import injector

container_context_dependencies: contextvars.ContextVar[dict[type, injector.Provider[Any]]] = contextvars.ContextVar(
    "container_context_dependencies"
)


class ContextScope(injector.Scope):
    def get(self, key: type, provider: injector.Provider[Any]) -> injector.Provider[Any]:
        context_dependencies: dict[type, injector.Provider[Any]] = self._get_context_dependencies()
        try:
            return context_dependencies[key]
        except KeyError:
            provider = injector.InstanceProvider(provider.get(self.injector))
            context_dependencies[key] = provider
            return provider

    def _get_context_dependencies(self) -> dict[type, injector.Provider[Any]]:
        try:
            return container_context_dependencies.get()
        except LookupError:
            container_context_dependencies.set({})
            return container_context_dependencies.get()


context_scope = injector.ScopeDecorator(ContextScope)
