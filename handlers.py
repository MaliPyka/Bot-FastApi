from database.requests import add_user, get_user
from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message


main_router = Router()

@main_router.message(Command("start"))
async def cmd_start(message: Message):
    res = await get_user(message.from_user.id)
    if not res:
        await add_user(message.from_user.id, message.from_user.username)
        await message.answer("Ты зарегистрирован!")
    else:
        await message.answer("Ты уже есть в базе!")

