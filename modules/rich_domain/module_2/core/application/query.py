from dataclasses import dataclass

import injector

from building_blocks.dto import DTO
from building_blocks.within_bounded_context.application.query import Query, QueryHandler
import modules.rich_domain.module_1.interface as module_1
from modules.rich_domain.ports.api_clients import CrudApiClient


class GetSomething(Query):
    param: str

    @dataclass(frozen=True)
    class Result(DTO):
        a: int
        b: str


class GetSomethingHandler(QueryHandler[GetSomething]):
    @injector.inject
    def __init__(self, crud_api_client: CrudApiClient):
        self._crud_api_client = crud_api_client

    async def handle(self, query: GetSomething) -> GetSomething.Result:
        a: module_1.GetA.Result = await module_1.get_module().message_bus.query(module_1.GetA())
        b = await self._crud_api_client.get_crud_data()
        return GetSomething.Result(a.a, b.domain_param + query.param)
