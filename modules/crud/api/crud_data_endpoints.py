from pydantic import BaseModel

from fastapi import APIRouter, Depends

import modules.crud.interface as crud_interface

router = APIRouter()


class CrudDataResp(BaseModel):
    a: int


@router.get("/crud", response_model=CrudDataResp)
async def get_crud_data(module: crud_interface.Module = Depends(crud_interface.get_module)):  # type: ignore[no-untyped-def]
    return await module.message_bus.query(module.GetCrudData())
