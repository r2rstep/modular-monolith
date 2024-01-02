import contextvars

import injector
import pytest

from infrastructure.container import scopes


@pytest.mark.asyncio()
class TestContextScope:
    class DummyDependency:
        ...

    @staticmethod
    @injector.provider
    @scopes.context_scope
    def dummy_provider() -> DummyDependency:
        return TestContextScope.DummyDependency()

    @pytest.fixture()
    def injector_(self):
        def configure(binder: injector.Binder) -> None:
            binder.bind(TestContextScope.DummyDependency, to=TestContextScope.dummy_provider)

        return injector.Injector(configure)

    async def test_single_context(self, injector_):
        # given context scope dependencies configured

        # when getting dependency
        dependency = injector_.get(TestContextScope.DummyDependency)

        # then dependency is of the requested type
        assert isinstance(dependency, TestContextScope.DummyDependency)

        # when getting the dependency again in the same context
        dependency2 = injector_.get(TestContextScope.DummyDependency)

        # then the same dependency is returned
        assert dependency is dependency2

    async def test_multiple_concurrent_contexts(self, injector_):
        # given context scope dependencies configured
        # and dependency for the current context
        dependency = injector_.get(TestContextScope.DummyDependency)

        # when creating a new context
        new_context = contextvars.Context()
        # and getting dependency in the new context
        dependency2 = new_context.run(injector_.get, TestContextScope.DummyDependency)

        # then the dependency is not the same as in the previous context
        assert dependency is not dependency2
