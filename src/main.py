from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.ad.router import router as router_announcement
from src.auth.router import router as router_auth
from src.pages.router import router as router_pages
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title='Advertisement App'
)

app.mount("/static", StaticFiles(directory="src/static"), name="static")
app.include_router(router_announcement)
app.include_router(router_auth)
app.include_router(router_pages)

origins = [
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)

# @app.on_event("startup")
# async def startup_event():
#     ...


