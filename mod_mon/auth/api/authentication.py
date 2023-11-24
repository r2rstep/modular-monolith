from pydantic import BaseModel, EmailStr, SecretStr

from fastapi import APIRouter

router = APIRouter()


class RegistrationReq(BaseModel):
    email: EmailStr
    password: SecretStr


@router.post("/register")
async def register(req: RegistrationReq) -> None:
    dict(req)
