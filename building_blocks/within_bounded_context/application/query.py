from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict

from building_blocks.dto import DTO


# using pydantic ensures query parameters are validated
class Query(ABC, BaseModel):
    model_config = ConfigDict(frozen=True)

    @dataclass(frozen=True)
    class Result(DTO):
        ...


QueryType = TypeVar("QueryType", bound=Query)


class QueryHandler(Generic[QueryType]):
    @abstractmethod
    async def handle(self, query: QueryType) -> DTO:
        ...
