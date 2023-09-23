from sqlalchemy import insert, select
from src.ad.models import Ad, AdType, AdCategory


async def get_all_types(session):
    query = select(AdType)
    result = await session.execute(query)
    result_list = []
    for value in result.all():
        ad_type = value[0].__dict__
        ad_type.pop('_sa_instance_state')
        result_list.append(ad_type)
    return result_list


async def add_type_ad(new_type_name, session):
    stmt = insert(AdType).values(name=new_type_name)
    await session.execute(stmt)
    await session.commit()


async def delete_type_ad(new_type_name, session):
    ...


async def get_all_category(session):
    query = select(AdCategory)
    result = await session.execute(query)
    result_list = []
    for value in result.all():
        ad_type = value[0].__dict__
        ad_type.pop('_sa_instance_state')
        result_list.append(ad_type)
    return result_list


async def add_category_ad(new_category_name, session):
    stmt = insert(AdCategory).values(name=new_category_name)
    await session.execute(stmt)
    await session.commit()


async def get_all_ad(session):
    query = select(Ad)
    result = await session.execute(query)
    result_list = []
    for value in result.all():
        ad_type = value[0].__dict__
        ad_type.pop('_sa_instance_state')
        result_list.append(ad_type)
    return result_list


async def add_new_ad(new_announcement, session):
    stmt = insert(Ad).values(**new_announcement.dict())
    await session.execute(stmt)
    await session.commit()


async def delete_ad():
    ...


async def update_ad():
    ...
