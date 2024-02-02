from dataclasses import dataclass

from building_blocks.dto import DTO
from building_blocks.within_bounded_context.application.query import Query, QueryHandler


class GetA(Query):
    @dataclass(frozen=True)
    class Result(DTO):
        a: int


class GetAHandler(QueryHandler[GetA]):
    async def handle(self, _: GetA) -> GetA.Result:
        return GetA.Result(1)
