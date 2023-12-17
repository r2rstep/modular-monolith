from uuid import UUID

from pydantic import BaseModel

from fastapi import APIRouter

from modules.rich_domain.module_1.core.commands.rich_domain_model import (
    CreateRichDomainModel,
    CreateRichDomainModelHandler,
)

from modules.rich_domain.module_1.infrastructure.container import Container

router = APIRouter()


class CreateRichDomainResourceReq(BaseModel):
    name: str


class CreatedRichDomainResourceResp(BaseModel):
    pk: UUID


@router.post("/", response_model=CreatedRichDomainResourceResp)
async def create_rich_domain_resource(req: CreateRichDomainResourceReq):
    container = Container()
    result = await CreateRichDomainModelHandler(container.event_bus).handle(CreateRichDomainModel(name=req.name))
    return {"pk": result}
