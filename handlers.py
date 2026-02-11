from database.requests import add_user, get_user, registration
from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from auth_utils import set_hashed_password

main_router = Router()

class Registration(StatesGroup):
    waiting_login = State()
    waiting_password = State()


@main_router.message(Command("start"))
async def cmd_start(message: Message):
    res = await get_user(message.from_user.id)
    if not res:
        await add_user(message.from_user.id, message.from_user.username)
        await message.answer("Ты зарегистрирован!")
    else:
        await message.answer("Ты уже есть в базе!")


@main_router.message(Command("reg"))
async def cmd_reg(message: Message, state: FSMContext):
    await message.answer("Введите логин:")
    await state.set_state(Registration.waiting_login)

@main_router.message(Registration.waiting_login)
async def cmd_reg(message: Message, state: FSMContext):
    await state.update_data(login=message.text)
    await message.answer("Введите пароль:")
    await state.set_state(Registration.waiting_password)

@main_router.message(Registration.waiting_password)
async def cmd_reg(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    data = await state.get_data()
    data['password'] = await set_hashed_password(data['password'])
    await registration(data['login'], data['password'], message.from_user.id)



