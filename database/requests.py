from aiogram.types import Update
from sqlalchemy import Insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy import update

from Schemas import BroadcastSchema, UserCreate
from database.models import async_session, User, Broadcast



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


async def insert_broadcast(text: str, count: int):
    async with async_session() as session:
        session.add(Broadcast(text=text, sent_count=count))
        await session.commit()

async def get_broadcast_history():
    async with async_session() as session:
        query = await session.execute(select(Broadcast))
        result = query.scalars().all()
        return result

async def registration(login: str, password: str, tg_id: int):
    async with async_session() as session:
        await session.execute(update(User).where(User.tg_id==tg_id).values(login=login,hashed_password=password))
        await session.commit()


async def get_hashed_password(login: str):
    async with async_session() as session:
        request = await session.execute(select(User.hashed_password).where(User.login==login))
        hashed_password = request.scalar()
        return hashed_password

async def get_all_logins():
    async with async_session() as session:
        query = await session.execute(select(User.login))
        return query.scalars().all()