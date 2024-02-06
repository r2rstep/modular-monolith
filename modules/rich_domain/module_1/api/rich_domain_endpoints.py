from uuid import UUID

from pydantic import BaseModel

from fastapi import APIRouter, Depends

from modules.rich_domain.module_1.interface import Module, get_module

router = APIRouter()


class CreateRichDomainResourceReq(BaseModel):
    name: str


class CreatedRichDomainResourceResp(BaseModel):
    pk: UUID


@router.post("/", response_model=CreatedRichDomainResourceResp)
async def create_rich_domain_resource(req: CreateRichDomainResourceReq, module: Module = Depends(get_module)):  # type: ignore[no-untyped-def]
    result = await module.message_bus.execute(module.CreateRichDomainModel(name=req.name))
    return {"pk": result}
