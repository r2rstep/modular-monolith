import contextvars
from typing import TypeVar

import injector

DependencyObject = TypeVar("DependencyObject")

container_context_dependencies: contextvars.ContextVar[
    dict[type[DependencyObject], DependencyObject]
] = contextvars.ContextVar("container_context_dependencies")


class ContextScope(injector.Scope):
    def get(self, key: type[DependencyObject], provider: injector.Provider[DependencyObject]) -> DependencyObject:
        context_dependencies = self._get_context_dependencies()
        try:
            return context_dependencies[key]
        except KeyError:
            provider = injector.InstanceProvider(provider.get(self.injector))
            context_dependencies[key] = provider
            return provider

    def _get_context_dependencies(self) -> dict[type[DependencyObject], DependencyObject]:
        try:
            return container_context_dependencies.get()
        except LookupError:
            container_context_dependencies.set({})
            return container_context_dependencies.get()


context_scope = injector.ScopeDecorator(ContextScope)
