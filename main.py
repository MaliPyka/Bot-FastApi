import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv

from database.models import engine, Base
from database.requests import get_all_users
from handlers import main_router
from ApiHandlers import api_router

load_dotenv()

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()
app = FastAPI()




@asynccontextmanager
async def lifespan(app: FastAPI):
    # Проверяем, не подключен ли роутер уже (защита от дублей при reload)
    if main_router not in dp.sub_routers:
        dp.include_router(main_router)
        logging.info("Main router included")

    app.include_router(api_router)

    # Создание таблиц
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Установка вебхука
    webhook_url = os.getenv("WEBHOOK_URL")
    if webhook_url:
        await bot.set_webhook(url=webhook_url)
        logging.info(f"Webhook URL set to {webhook_url}")
    else:
        logging.warning("WEBHOOK_URL not found in .env")

    yield

    # Закрытие сессий
    await bot.delete_webhook()
    await bot.session.close()

app = FastAPI(lifespan=lifespan)


@app.post("/webhook")
async def bot_webhook(request: Request):
    update_data = await request.json()
    if update_data is None:
        return {"error": "Empty payload"}

    update = types.Update(**update_data)
    await dp.feed_update(bot, update)
    return {"ok": True}

if __name__ == "__main__":
    import uvicorn
    logging.basicConfig(level=logging.INFO)
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)



