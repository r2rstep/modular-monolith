from fastapi import FastAPI

from mod_mon.auth.api import authentication

app = FastAPI(title="mod_mon API", version="0.1.0")

app.include_router(authentication.router, prefix="/auth")
