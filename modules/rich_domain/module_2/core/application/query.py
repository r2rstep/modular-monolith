from dataclasses import dataclass

import injector

from modules.rich_domain.module_2.core.application.bases import Query
from modules.rich_domain.module_2.core.types import Module1

from building_blocks.dto import DTO
from building_blocks.within_bounded_context.application.query import QueryHandler
import modules.rich_domain.module_1.interface as module_1
from modules.rich_domain.ports.api_clients import CrudApiClient


class GetSomething(Query["GetSomething.Result"]):
    param: str

    @dataclass(frozen=True)
    class Result(DTO):
        a: int
        b: str


class GetSomethingHandler(QueryHandler[GetSomething]):
    @injector.inject
    def __init__(self, crud_api_client: CrudApiClient, module_1_interface: Module1):
        self._crud_api_client = crud_api_client
        self._module_1 = module_1_interface

    async def handle(self, query: GetSomething) -> GetSomething.Result:
        a: module_1.GetA.Result = await self._module_1.GetA().handle()
        b = await self._crud_api_client.get_crud_data()
        return GetSomething.Result(a.a, b.domain_param + query.param)
