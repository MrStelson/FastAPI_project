from fastapi import FastAPI
from src.ad.router import router as router_announcement
from fastapi.staticfiles import StaticFiles


app = FastAPI(
    title='Ad App'
)

# app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(router_announcement)


# @app.on_event("startup")
# async def startup_event():
#     ...

