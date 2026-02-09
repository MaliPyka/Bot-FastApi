from sqlalchemy import Insert, select
from sqlalchemy.exc import IntegrityError

from database.models import async_session, User



async def add_user(tg_id: int, username: str):
    async with async_session() as session:
        session.add(User(tg_id=tg_id, username=username))
        await session.commit()

async def get_user(tg_id: int):
    async with async_session() as session:
        query = select(User).where(User.tg_id==tg_id)
        user = await session.scalar(query)
        return user


async def get_all_users():
    async with async_session() as session:
        query = await session.execute(select(User))
        users = query.scalars(query).all()
        return users



