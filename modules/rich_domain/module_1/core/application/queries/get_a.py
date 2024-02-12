from dataclasses import dataclass

from modules.rich_domain.module_1.core.application.bases import Query

from building_blocks.application.query import QueryHandler
from building_blocks.dto import DTO


class GetA(Query["GetA.Result"]):
    @dataclass(frozen=True)
    class Result(DTO):
        a: int


class GetAHandler(QueryHandler[GetA]):
    async def handle(self, _: GetA) -> GetA.Result:
        return GetA.Result(1)
