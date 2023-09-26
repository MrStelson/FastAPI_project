from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.ad.schemas import AdCreate, AdComments, AdComplaint, AdUpdate
from src.ad.service import *

from src.config import API_URL
from src.database import get_async_session

from src.auth.config import current_user
from src.auth.models import User

router = APIRouter(
    prefix=f'/{API_URL}/ad',
    tags=['Ad'],
)


@router.get('/type')
async def get_type(session: AsyncSession = Depends(get_async_session)):
    try:
        result = await get_all_types(session=session)
        return {
            "status": 200,
            "data": result,
            "detail": None,
        }
    except Exception:
        return {
            "status": 500,
            "data": f"Internal Server Error",
            "detail": None,
        }


@router.get('/types/{type_id}')
async def get_type_id(type_id: int,
                      session: AsyncSession = Depends(get_async_session)
                      ):
    try:
        result = await get_type_by_id(type_id=type_id, session=session)
        return {
            "status": 200,
            "data": result,
            "detail": None,
        }
    except Exception:
        return {
            "status": 500,
            "data": f"Internal Server Error",
            "detail": None,
        }


@router.get('/types/{type_slug}')
async def get_type_slug(type_slug: str,
                        session: AsyncSession = Depends(get_async_session)
                        ):
    try:
        result = await get_type_by_slug(type_slug=type_slug, session=session)
        return {
            "status": 200,
            "data": result,
            "detail": None,
        }
    except Exception:
        return {
            "status": 500,
            "data": f"Internal Server Error",
            "detail": None,
        }


@router.post('/type')
async def add_type(new_type_name: str,
                   session: AsyncSession = Depends(get_async_session),
                   user: User = Depends(current_user),
                   ):
    if user is None:
        return {
            "status": 401,
            "data": None,
            "detail": "Don't have access. Please authorisation"
        }
    if user.role_id in [2, 3]:
        try:
            await add_type_ad(new_type_name, session)
            return {
                "status": 200,
                "data": f"type {new_type_name} added",
                "detail": None,
            }
        except Exception:
            return {
                "status": 500,
                "data": f"Internal Server Error",
                "detail": None,
            }
    else:
        return {
            "status": 401,
            "data": None,
            "detail": "Don't have access"
        }


@router.get('/category')
async def get_category(session: AsyncSession = Depends(get_async_session)):
    try:
        result = await get_all_category(session=session)
        return {
            "status": 200,
            "data": result,
            "detail": None,
        }
    except Exception:
        return {
            "status": 500,
            "data": f"Internal Server Error",
            "detail": None,
        }


@router.post('/category')
async def add_category(new_category_name: str,
                       type_id: int,
                       session: AsyncSession = Depends(get_async_session),
                       user: User = Depends(current_user),
                       ):
    if user is None:
        return {
            "status": 401,
            "data": None,
            "detail": "Don't have access. Please authorisation"
        }
    if user.role_id in [2, 3]:
        try:
            await add_category_ad(new_category_name, type_id, session)
            return {
                "status": 200,
                "data": f"Category {new_category_name} added",
                "detail": None,
            }
        except Exception:
            return {
                "status": 500,
                "data": f"Internal Server Error",
                "detail": None,
            }
    else:
        return {
            "status": 401,
            "data": None,
            "detail": "Don't have access"
        }


@router.get('/')
async def get_ad(session: AsyncSession = Depends(get_async_session),
                 page: int = 0,
                 size: int = 10,
                 ):
    try:
        result = await get_all_ad(session=session, page=page, size=size)
        return {
            "status": 200,
            "data": result,
            "detail": None,
        }
    except Exception:
        return {
            "status": 500,
            "data": f"Internal Server Error",
            "detail": None,
        }


@router.put('/update/{ad_id}')
async def update_ad(ad_id: int,
                    updated_ad: AdUpdate,
                    user: User = Depends(current_user),
                    session: AsyncSession = Depends(get_async_session)):
    if user is None:
        return {
            "status": 401,
            "data": None,
            "detail": "Don't have access. Please authorisation"
        }
    if user.is_banned:
        return {
            "status": 401,
            "data": None,
            "detail": "You banned"
        }
    try:
        updated_ad.updated_at = datetime.utcnow()
        await update_new_ad(ad_id, updated_ad, user_id=user.id, session=session)
        return {
            "status": 200,
            "data": f'Advertisement {updated_ad.name} updated',
            "detail": None,
        }
    except Exception:
        return {
            "status": 500,
            "data": f"Internal Server Error",
            "detail": None,
        }


@router.get('/{ad_id}')
async def get_ad_by_id(ad_id: int,
                       session: AsyncSession = Depends(get_async_session),
                       ):
    try:
        result = await get_one_ad(ad_id=ad_id, session=session)
        return {
            "status": 200,
            "data": result,
            "detail": None,
        }
    except Exception:
        return {
            "status": 500,
            "data": f"Internal Server Error",
            "detail": None,
        }


@router.get('/type/{type_id}')
async def get_ad_by_type(type_id: int,
                         session: AsyncSession = Depends(get_async_session),
                         page: int = 0,
                         size: int = 5,
                         ):
    try:
        result = await get_by_type(type_id=type_id, session=session, page=page, size=size)
        return {
            "status": 200,
            "data": result,
            "detail": None,
        }
    except Exception:
        return {
            "status": 500,
            "data": f"Internal Server Error",
            "detail": None,
        }


@router.get('/type/{type_slug}')
async def get_ad_by_type(type_slug: str,
                         session: AsyncSession = Depends(get_async_session),
                         page: int = 0,
                         size: int = 5,
                         ):
    try:
        result = await get_by_type_slug(type_slug=type_slug, session=session, page=page, size=size)
        return {
            "status": 200,
            "data": result,
            "detail": None,
        }
    except Exception:
        return {
            "status": 500,
            "data": f"Internal Server Error",
            "detail": None,
        }


@router.get('/category/{category_name}')
async def get_ad_by_category(category_name: str,
                             session: AsyncSession = Depends(get_async_session),
                             ):
    try:
        result = await get_by_category(category_name=category_name, session=session)
        return {
            "status": 200,
            "data": result,
            "detail": None,
        }
    except Exception:
        return {
            "status": 500,
            "data": f"Internal Server Error",
            "detail": None,
        }


@router.get('/user/{user_id}')
async def get_ad_by_id_user(user_id: int,
                            session: AsyncSession = Depends(get_async_session),
                            ):
    try:
        result = await get_by_user_id(user_id=user_id, session=session)
        return {
            "status": 200,
            "data": result,
            "detail": None,
        }
    except Exception:
        return {
            "status": 500,
            "data": f"Internal Server Error",
            "detail": None,
        }


@router.post('/')
async def add_ad(new_ad: AdCreate,
                 session: AsyncSession = Depends(get_async_session),
                 user: User = Depends(current_user),
                 ):
    if user is None:
        return {
            "status": 401,
            "data": None,
            "detail": "Don't have access. Please authorisation"
        }
    if user.is_banned:
        return {
            "status": 401,
            "data": None,
            "detail": "Your banned"
        }
    try:
        new_ad.user_id = user.id
        await add_new_ad(new_ad, session)
        return {
            "status": 200,
            "data": f'Advertisement {new_ad.name} added',
            "detail": None,
        }
    except Exception:
        return {
            "status": 500,
            "data": f"Internal Server Error",
            "detail": None,
        }


@router.delete('/delete/{ad_id}')
async def delete_ad(ad_id: int,
                    session: AsyncSession = Depends(get_async_session),
                    user: User = Depends(current_user),
                    ):
    if user is None:
        return {
            "status": 401,
            "data": None,
            "detail": "Don't have access. Please authorisation"
        }
    try:
        await delete_ad_db(ad_id=ad_id, user_id=user.id, session=session)
        return {
            "status": 200,
            "data": f'Advertisement deleted',
            "detail": None,
        }
    except ValueError:
        return {
            "status": 401,
            "data": None,
            "detail": "Don't have access"
        }
    except Exception:
        return {
            "status": 500,
            "data": f"Internal Server Error",
            "detail": None,
        }


@router.get('/{ad_id}/comments')
async def get_ad_comments(ad_id: int,
                          session: AsyncSession = Depends(get_async_session),
                          ):
    try:
        result = await get_comments(ad_id=ad_id, session=session)
        return {
            "status": 200,
            "data": result,
            "detail": None,
        }
    except Exception:
        return {
            "status": 500,
            "data": f"Internal Server Error",
            "detail": None,
        }


@router.post('/{ad_id}/comments')
async def add_ad_comments(ad_id: int,
                          value: str,
                          session: AsyncSession = Depends(get_async_session),
                          user: User = Depends(current_user),
                          ):
    if user is None:
        return {
            "status": 401,
            "data": None,
            "detail": "Don't have access. Please authorisation"
        }
    try:
        new_comment = AdComments(
            ad_id=ad_id,
            value=value,
            user_id=user.id
        )
        await add_comment(new_comment, session=session)
        return {
            "status": 200,
            "data": f'Comment added',
            "detail": None,
        }
    except Exception:
        return {
            "status": 500,
            "data": f"Internal Server Error",
            "detail": None,
        }


@router.delete('/{ad_id}/comments/delete/{comment_id}')
async def delete_ad_comment(comment_id: int,
                            session: AsyncSession = Depends(get_async_session),
                            user: User = Depends(current_user), ):
    if user is None:
        return {
            "status": 401,
            "data": None,
            "detail": "Don't have access. Please authorisation"
        }
    if user.role_id in [2, 3]:
        try:
            await delete_comment(comment_id=comment_id, session=session)
            return {
                "status": 200,
                "data": f'Comment deleted',
                "detail": None,
            }
        except Exception:
            return {
                "status": 500,
                "data": f"Internal Server Error",
                "detail": None,
            }


@router.post('/{ad_id}/complaint')
async def add_ad_complaint(ad_id: int,
                           value: str,
                           session: AsyncSession = Depends(get_async_session),
                           user: User = Depends(current_user),
                           ):
    if user is None:
        return {
            "status": 401,
            "data": None,
            "detail": "Don't have access. Please authorisation"
        }
    try:
        new_complaint = AdComplaint(
            ad_id=ad_id,
            value=value,
            user_id=user.id
        )
        await add_complaint(new_complaint, session=session)
        return {
            "status": 200,
            "data": f'Comment added',
            "detail": None,
        }
    except Exception:
        return {
            "status": 500,
            "data": f"Internal Server Error",
            "detail": None,
        }


@router.get('/{ad_id}/complaint')
async def get_ad_complaint(ad_id: int,
                           session: AsyncSession = Depends(get_async_session),
                           user: User = Depends(current_user),
                           ):
    if user is None:
        return {
            "status": 401,
            "data": None,
            "detail": "Don't have access. Please authorisation"
        }
    if user.role_id in [2, 3]:
        try:
            result = await get_complaint(ad_id=ad_id, session=session)
            return {
                "status": 200,
                "data": result,
                "detail": None,
            }
        except Exception:
            return {
                "status": 500,
                "data": f"Internal Server Error",
                "detail": None,
            }
    return {
        "status": 401,
        "data": None,
        "detail": "Don't have access"
    }
