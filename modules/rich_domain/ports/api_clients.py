from abc import ABC, abstractmethod
from dataclasses import dataclass

from building_blocks.dto import DTO


@dataclass(frozen=True)
class CrudData(DTO):
    domain_param: str


class CrudApiClient(ABC):
    @abstractmethod
    async def get_crud_data(self) -> CrudData:
        ...
