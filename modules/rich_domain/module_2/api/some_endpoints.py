from typing import Annotated

from pydantic import BaseModel

from fastapi import APIRouter, Query

from modules.rich_domain.module_2.interface import GetSomething, get_module

router = APIRouter()


class SomeResp(BaseModel):
    a: int
    b: str


@router.get("/some-endpoint")
async def some_endpoint(param: Annotated[str, Query(...)]):  # type: ignore[no-untyped-def]
    return await get_module().message_bus.query(GetSomething(param=param))
