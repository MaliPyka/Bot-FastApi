from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from database.models import User, async_session
from database.requests import get_all_users


api_router = APIRouter(
    prefix="/users",
    tags=["Users Management"])


@api_router.get("/users")
async def cmd_get_users():
    result = await get_all_users()
    return {"users": result}