from fastapi import APIRouter

from src.auth.config import fastapi_users, auth_backend
from src.auth.schemas import UserRead, UserCreate

from src.config import API_URL

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix=f"/{API_URL}/auth/jwt",
    tags=["Auth"],
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix=f"/{API_URL}/auth",
    tags=["Auth"],
)

