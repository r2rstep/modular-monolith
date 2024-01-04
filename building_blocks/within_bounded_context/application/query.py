from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict

from building_blocks.dto import DTO


# using pydantic ensures query parameters are validated
class Query(ABC, BaseModel):
    model_config = ConfigDict(frozen=True)


QueryType = TypeVar("QueryType", bound=Query)
QueryReturnType = TypeVar("QueryReturnType", bound=DTO)


class QueryHandler(Generic[QueryType, QueryReturnType]):
    @abstractmethod
    def handle(self, query: QueryType) -> QueryReturnType:
        ...
