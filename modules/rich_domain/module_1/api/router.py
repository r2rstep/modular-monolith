from fastapi import APIRouter

from modules.rich_domain.module_1.api.rich_domain_endpoints import router as rich_domain_resource_router

router = APIRouter()
router.include_router(rich_domain_resource_router, prefix="/rich_domain_resources")
