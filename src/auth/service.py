from fastapi import Depends
from sqlalchemy import insert, select, delete, update
from src.auth.models import User
from src.database import get_async_session, async_session_maker
from sqlalchemy.ext.asyncio import AsyncSession


async def get_result_list(query, session):
    result = await session.execute(query)
    result_list = []
    for value in result.all():
        ad_type = value[0].__dict__
        ad_type.pop('_sa_instance_state')
        result_list.append(ad_type)
    return result_list


async def get_all_users(session: AsyncSession = Depends(get_async_session)):
    query = select(User).order_by(User.id)
    result_list = await get_result_list(query=query, session=session)
    return result_list


async def banned_users(user_id: int):
    async with async_session_maker() as session:
        user = await session.execute(select(User).where(User.id == user_id))
        stmt = update(User).where(User.id == user_id).values(is_banned=not user.first()[0].is_banned)
        await session.execute(stmt)
        await session.commit()


async def add_admin(user_id: int):
    async with async_session_maker() as session:
        stmt = update(User).where(User.id == user_id).values(role_id=3)
        await session.execute(stmt)
        await session.commit()
