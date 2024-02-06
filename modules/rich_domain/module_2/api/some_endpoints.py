from typing import Annotated

from pydantic import BaseModel

from fastapi import APIRouter, Depends, Query

from modules.rich_domain.module_2.interface import Module, get_module

router = APIRouter()


class SomeResp(BaseModel):
    a: int
    b: str


@router.get("/some-endpoint")
async def some_endpoint(param: Annotated[str, Query(...)], module: Module = Depends(get_module)):  # type: ignore[no-untyped-def] # noqa: B008
    return await module.message_bus.query(module.GetSomething(param=param))
