from uuid import UUID

from pydantic import BaseModel

from fastapi import APIRouter

from modules.rich_domain.module_1.core.application.commands.rich_domain_model import CreateRichDomainModel

from modules.rich_domain.module_1.interface import module_1

router = APIRouter()


class CreateRichDomainResourceReq(BaseModel):
    name: str


class CreatedRichDomainResourceResp(BaseModel):
    pk: UUID


@router.post("/", response_model=CreatedRichDomainResourceResp)
async def create_rich_domain_resource(req: CreateRichDomainResourceReq):  # type: ignore[no-untyped-def]
    result = await module_1.command_bus.execute(CreateRichDomainModel(name=req.name))
    return {"pk": result}
