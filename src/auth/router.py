from fastapi import APIRouter, Depends

from src.auth.config import fastapi_users, auth_backend, current_user
from src.auth.models import User
from src.auth.schemas import UserRead, UserCreate
from src.auth.service import banned_users, add_admin

from src.config import API_URL

router = APIRouter(
    prefix=f"/{API_URL}",
    tags=["Auth"],
)

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix=f"/auth/jwt",
    tags=["Auth"],
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix=f"/auth",
    tags=["Auth"],
)


@router.post('/auth/banned/{user_id}')
async def banned_user(user_id: int,
                      user: User = Depends(current_user)):
    if user is None:
        return {
            "status": 401,
            "data": None,
            "detail": "Don't have access. Please authorisation"
        }
    if user.role_id == 3:
        try:
            await banned_users(user_id)
            return {
                "status": 200,
                "data": f'User with id={user_id} banned',
                "detail": None,
            }
        except Exception:
            return {
                "status": 500,
                "data": f"Internal Server Error",
                "detail": None,
            }


@router.post('/auth/make_admin/{user_id}')
async def make_admin_user(user_id: int,
                          user: User = Depends(current_user)):
    if user is None:
        return {
            "status": 401,
            "data": None,
            "detail": "Don't have access. Please authorisation"
        }
    if user.role_id == 3:
        try:
            await add_admin(user_id)
            return {
                "status": 200,
                "data": f'User with id={user_id} admin',
                "detail": None,
            }
        except Exception:
            return {
                "status": 500,
                "data": f"Internal Server Error",
                "detail": None,
            }
