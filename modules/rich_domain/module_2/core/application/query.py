from dataclasses import dataclass

from building_blocks.dto import DTO
from building_blocks.within_bounded_context.application.query import Query, QueryHandler
import modules.rich_domain.module_1.interface as module_1


class GetSomething(Query):
    param: str

    @dataclass(frozen=True)
    class Result(DTO):
        a: int
        b: str


class GetSomethingHandler(QueryHandler[GetSomething]):
    async def handle(self, query: GetSomething) -> GetSomething.Result:
        a: module_1.GetA.Result = await module_1.get_module().command_bus.query(module_1.GetA())
        return GetSomething.Result(a.a, query.param)
