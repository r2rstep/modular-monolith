from contextlib import AbstractAsyncContextManager, asynccontextmanager

from fastapi import FastAPI

from app.infrastructure.startup import start_modules
from modules.rich_domain import module_1


@asynccontextmanager
async def app_lifespan(_: FastAPI) -> AbstractAsyncContextManager[None]:
    start_modules()

    yield


app = FastAPI(title="mod_mon API", version="0.1.0", lifespan=app_lifespan)

for router in module_1.startup.get_routers():
    app.include_router(router)
