from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.ad.schemas import AdCreate
from src.ad.service import *

from src.config import API_URL
from src.database import get_async_session

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


@router.post('/type')
async def add_type(new_type_name: str,
                   session: AsyncSession = Depends(get_async_session),
                   ):
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
                       session: AsyncSession = Depends(get_async_session),
                       ):
    try:
        await add_category_ad(new_category_name, session)
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


@router.get('/')
async def get_ad(session: AsyncSession = Depends(get_async_session)):
    try:
        result = await get_all_ad(session=session)
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
                 session: AsyncSession = Depends(get_async_session)
                 ):
    try:
        await add_new_ad(new_ad, session=session)
        return {
            "status": 200,
            "data": f'announcement {new_ad.name} added',
            "detail": None,
        }
    except Exception:
        return {
            "status": 500,
            "data": f"Internal Server Error",
            "detail": None,
        }
