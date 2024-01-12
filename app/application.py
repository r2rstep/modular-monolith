from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI

from app.infrastructure.startup import start_modules
from commons.messagebox.application.process_messagebox import ProcessInbox
from modules.rich_domain import module_1, module_2


@asynccontextmanager
async def app_lifespan(_: FastAPI) -> AsyncIterator[None]:
    start_modules()

    yield


# TODO @R2RStep: implement proper inbox processing
# https://github.com/r2rstep/modular-monolith/issues/20
async def process_inboxes() -> None:
    await module_1.interface.get_module().command_bus.execute(ProcessInbox())
    await module_2.interface.get_module().command_bus.execute(ProcessInbox())


app = FastAPI(title="mod_mon API", version="0.1.0", lifespan=app_lifespan, dependencies=[Depends(process_inboxes)])

for router in module_1.startup.get_routers():
    app.include_router(router)
