from uuid import UUID

from pydantic import BaseModel

from fastapi import APIRouter

from modules.rich_domain.module_1.core.application.commands.rich_domain_model import CreateRichDomainModel

from modules.rich_domain.module_1.interface import get_module

router = APIRouter()


class CreateRichDomainResourceReq(BaseModel):
    name: str


class CreatedRichDomainResourceResp(BaseModel):
    pk: UUID


@router.post("/", response_model=CreatedRichDomainResourceResp)
async def create_rich_domain_resource(req: CreateRichDomainResourceReq):  # type: ignore[no-untyped-def]
    result = await get_module().message_bus.execute(CreateRichDomainModel(name=req.name))
    return {"pk": result}
