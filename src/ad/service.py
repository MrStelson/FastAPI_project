from sqlalchemy import insert, select, delete, update
from src.ad.models import Ad, AdType, AdCategory, AdComment, AdComplaint
from src.database import async_session_maker


async def get_result_list(query,
                          session,
                          page: int = 0,
                          size: int = 5,
                          ):
    # print(query)
    offset_min = page * size
    offset_max = (page + 1) * size
    result = await session.execute(query)
    result_list = []
    res = result.all()[offset_min:offset_max]
    for value in res:
        row = value[0].__dict__
        row.pop('_sa_instance_state')
        result_list.append(row)
    return result_list


async def get_all_types():
    async with async_session_maker() as session:
        query = select(AdType)
        result_list = await get_result_list(query=query, session=session, size=1000)
        return result_list


async def get_type_by_id(type_id):
    async with async_session_maker() as session:
        query = select(AdType).where(AdType.id == type_id)
        result_list = await get_result_list(query=query, session=session)
        return result_list


async def get_type_by_name(type_name):
    async with async_session_maker() as session:
        query = select(AdType).where(AdType.type_name == type_name)
        result_list = await get_result_list(query=query, session=session)
        type_id = result_list[0]
        return type_id["id"]


async def add_type_ad(new_type_name):
    async with async_session_maker() as session:
        stmt = insert(AdType).values(type_name=new_type_name)
        await session.execute(stmt)
        await session.commit()


async def get_all_category():
    async with async_session_maker() as session:
        query = select(AdCategory)
        result_list = await get_result_list(query=query, session=session, size=1000)
        return result_list


async def get_category_by_name(category_name):
    async with async_session_maker() as session:
        query = select(AdCategory).where(AdCategory.category_name == category_name)
        result_list = await get_result_list(query=query, session=session)
        category_id = result_list[0]
        return category_id["id"]


async def add_category_ad(new_category_name, type_id):
    async with async_session_maker() as session:
        stmt = insert(AdCategory).values(type_id=type_id, name=new_category_name)
        await session.execute(stmt)
        await session.commit()


async def get_all_ad(page: int, size: int, ):
    async with async_session_maker() as session:
        query = select(Ad).join(AdCategory).join(AdType).order_by(-Ad.id)
        result_list = await get_result_list(query=query, session=session, page=page, size=size)
        return result_list


async def get_one_ad(ad_id):
    async with async_session_maker() as session:
        query = select(Ad, AdCategory, AdType). \
            join(AdCategory, Ad.category_id == AdCategory.id). \
            join(AdType, AdCategory.type_id == AdType.id). \
            where(Ad.id == ad_id)
        result = await session.execute(query)
        res = result.all()
        result_list = []
        for row in res[0]:
            value = row.__dict__
            value.pop('_sa_instance_state')
            result_list.append(value)
        return result_list


async def get_by_category(category_name):
    async with async_session_maker() as session:
        query = select(Ad).join(AdCategory).where(AdCategory.name == category_name)
        result_list = await get_result_list(query=query, session=session)
        return result_list


async def get_by_type(type_id, page: int, size: int):
    async with async_session_maker() as session:
        query = select(Ad).join(AdCategory).join(AdType).where(AdType.id == type_id)
        result_list = await get_result_list(query=query, session=session, page=page, size=size)
        return result_list


async def get_by_user_id(user_id):
    async with async_session_maker() as session:
        query = select(Ad).where(Ad.user_id == user_id)
        result_list = await get_result_list(query=query, session=session)
        return result_list


async def add_new_ad(new_announcement):
    async with async_session_maker() as session:
        stmt = insert(Ad).values(**new_announcement.dict())
        print(stmt)
        await session.execute(stmt)
        await session.commit()


async def update_new_ad(ad_id, updated_ad, user_id):
    async with async_session_maker() as session:
        query = select(Ad).where(Ad.id == ad_id)
        result = await session.execute(query)
        ad = result.first()[0]
        if ad.user_id == user_id:
            stmt = update(Ad).where(Ad.id == ad_id).values(**updated_ad.dict())
            await session.execute(stmt)
            await session.commit()
        else:
            raise ValueError()


async def delete_ad_db(ad_id, user):
    async with async_session_maker() as session:
        query = select(Ad).where(Ad.id == ad_id)
        result = await session.execute(query)
        ad = result.first()[0]
        if (ad.user_id == user.id) or (user.role_id in [2, 3]):
            stmt = delete(Ad).where(Ad.id == ad_id)
            await session.execute(stmt)
            await session.commit()
        else:
            raise ValueError()


async def update_ad():
    ...


async def get_comments(ad_id):
    async with async_session_maker() as session:
        query = select(AdComment).join(Ad).where(AdComment.ad_id == ad_id).order_by(-AdComment.id)
        result_list = await get_result_list(query=query, session=session)
        return result_list


async def add_comment(new_comment):
    async with async_session_maker() as session:
        stmt = insert(AdComment).values(**new_comment.dict())
        await session.execute(stmt)
        await session.commit()


async def delete_comment(comment_id):
    async with async_session_maker() as session:
        stmt = delete(AdComment).where(AdComment.id == comment_id)
        await session.execute(stmt)


async def get_complaint(ad_id):
    async with async_session_maker() as session:
        query = select(AdComplaint).join(Ad).where(AdComplaint.ad_id == ad_id).order_by(AdComplaint.id)
        result_list = await get_result_list(query=query, session=session)
        return result_list


async def add_complaint(new_complaint):
    async with async_session_maker() as session:
        stmt = insert(AdComment).values(**new_complaint.dict())
        await session.execute(stmt)
        await session.commit()
