from fastapi import FastAPI
from src.ad.router import router as router_announcement
from src.auth.router import router as router_auth
from fastapi.staticfiles import StaticFiles

from src.auth.schemas import UserRead, UserCreate

app = FastAPI(
    title='Advertisement App'
)

# app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(router_announcement)
app.include_router(router_auth)

# @app.on_event("startup")
# async def startup_event():
#     ...
