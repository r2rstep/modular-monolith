from dataclasses import dataclass

from modules.crud.core.application.bases import Query

from building_blocks.application.query import QueryHandler
from building_blocks.dto import DTO


class GetCrudData(Query["GetCrudData.Result"]):
    @dataclass(frozen=True)
    class Result(DTO):
        a: int


class GetCrudDataHandler(QueryHandler[GetCrudData]):
    async def handle(self, _: GetCrudData) -> GetCrudData.Result:
        return GetCrudData.Result(1)
