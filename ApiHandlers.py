from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from Schemas import BroadcastSchema, UserCreate
from database.models import User, async_session
from database.requests import get_all_users, insert_broadcast, get_broadcast_history, get_all_logins, get_hashed_password
from config import bot
from auth_utils import verify_hashed_password
from auth import create_access_token, get_current_user
from fastapi import Response, Depends

api_router = APIRouter(
    prefix="/users",
    tags=["Users Management"])


@api_router.get("/users")
async def cmd_get_users():
    result = await get_all_users()
    return {"users": result}


@api_router.post("/broadcast")
async def cmd_broadcast_user(data: BroadcastSchema, user: str = Depends(get_current_user)):
    async with async_session() as session:
        print(user)
        result = await session.execute(select(User.tg_id))
        users = result.scalars().all()

        count = 0

        for user_id in users:
            try:
                await bot.send_message(chat_id=user_id, text=data.text)
                count += 1
            except Exception as e:
                print(f"Не удалось отправить сообщение {user_id}: {e}")

        await insert_broadcast(data.text, count)
        return {"status": "success", "sent_to": count, "total_users": len(users)}


@api_router.get("/broadcast/list")
async def cmd_broadcast_list():
    broadcast_history = await get_broadcast_history()
    return {"broadcast_history": broadcast_history}

@api_router.post("/registration")
async def cmd_registration(data: UserCreate, response: Response):
    logins = await get_all_logins()
    if data.login in logins:
        hashed_password = await get_hashed_password(data.login)
        if verify_hashed_password(data.password, hashed_password):
            token = create_access_token({"sub": data.login})
            response.set_cookie(
                key="access_token",
                value=token,
                httponly=True,
                samesite="lax",
            )

            return {
                "status": "success",
                "access_token": token,
            }
        else:
            return {"status": "failed", "message": "Wrong password"}
    else:
        return {"status": "failed", "message": "Wrong login"}