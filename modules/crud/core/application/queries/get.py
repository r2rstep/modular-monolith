from dataclasses import dataclass

from building_blocks.dto import DTO
from building_blocks.within_bounded_context.application.query import Query, QueryHandler


class GetCrudData(Query):
    @dataclass(frozen=True)
    class Result(DTO):
        a: int


class GetCrudDataHandler(QueryHandler[GetCrudData]):
    async def handle(self, _: GetCrudData) -> GetCrudData.Result:
        return GetCrudData.Result(1)
