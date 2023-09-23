from sqlalchemy import insert, select, delete
from src.ad.models import Ad, AdType, AdCategory, AdComment


async def get_result_list(query, session):
    result = await session.execute(query)
    result_list = []
    for value in result.all():
        ad_type = value[0].__dict__
        ad_type.pop('_sa_instance_state')
        result_list.append(ad_type)
    return result_list


async def get_all_types(session):
    query = select(AdType)
    result_list = await get_result_list(query=query, session=session)
    return result_list


async def add_type_ad(new_type_name, session):
    stmt = insert(AdType).values(type_name=new_type_name)
    await session.execute(stmt)
    await session.commit()


async def get_all_category(session):
    query = select(AdCategory)
    result_list = await get_result_list(query=query, session=session)
    return result_list


async def add_category_ad(new_category_name, session):
    stmt = insert(AdCategory).values(name=new_category_name)
    await session.execute(stmt)
    await session.commit()


async def get_all_ad(session):
    query = select(Ad)
    result_list = await get_result_list(query=query, session=session)
    return result_list


async def get_one_ad(ad_id, session):
    query = select(Ad).where(Ad.id == ad_id)
    result = await session.execute(query)
    result = result.first()[0]
    return result.__dict__


async def get_by_category(category_name, session):
    query = select(Ad).join(AdCategory).where(AdCategory.name == category_name)
    result_list = await get_result_list(query=query, session=session)
    return result_list


async def get_by_type(type_name, session):
    query = select(Ad).join(AdType).where(AdType.type_name == type_name)
    result_list = await get_result_list(query=query, session=session)
    return result_list


async def add_new_ad(new_announcement, session):
    stmt = insert(Ad).values(**new_announcement.dict())
    await session.execute(stmt)
    await session.commit()


async def delete_ad_db(ad_id, user_id, session):
    query = select(Ad).where(Ad.id == ad_id)
    result = await session.execute(query)
    ad = result.first()[0]
    if ad.user_id == user_id:
        stmt = delete(Ad).where(Ad.id == ad_id)
        await session.execute(stmt)
        await session.commit()
    else:
        raise ValueError()


async def update_ad():
    ...


async def get_comments(ad_id, session):
    query = select(AdComment).join(Ad).where(AdComment.ad_id == ad_id)
    result_list = await get_result_list(query=query, session=session)
    return result_list


async def add_comment(new_comment, session):
    stmt = insert(AdComment).values(**new_comment.dict())
    await session.execute(stmt)
    await session.commit()


async def delete_comment(comment_id, session):
    stmt = delete(AdComment).where(AdComment.id == comment_id)
    await session.execute(stmt)
