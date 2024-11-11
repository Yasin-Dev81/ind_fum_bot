import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, enums
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiostep import Listen
from aiohttp import web
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from middlewares.db_check import DBCheck
from handlers import setup_routers
from app import setup_routes
from tasks import register
from config import (
    BOT_TOKEN,
    WEBHOOK_URL,
    PORT,
    TIME_ZONE,
)
import glv


glv.bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode=enums.ParseMode.HTML))
glv.storage = MemoryStorage()
glv.dp = Dispatcher(storage=glv.storage)
app = web.Application()
aioscheduler = AsyncIOScheduler(timezone=TIME_ZONE)

logging.basicConfig(level=logging.INFO, stream=sys.stdout)


async def on_startup(app: web.Application):
    await glv.bot.set_webhook(f"{WEBHOOK_URL}/webhook")
    register(aioscheduler)


def setup_middlewares():
    glv.dp.message.outer_middleware(DBCheck())
    glv.dp.callback_query.outer_middleware(DBCheck())
    glv.dp.message.outer_middleware(Listen())


async def main():
    setup_routers(glv.dp)
    setup_middlewares()

    glv.dp.startup.register(on_startup)

    setup_routes(app)

    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=glv.dp,
        bot=glv.bot,
    )
    webhook_requests_handler.register(app, path="/webhook")

    setup_application(app, glv.dp, bot=glv.bot)
    await web._run_app(app, host="0.0.0.0", port=PORT)


if __name__ == "__main__":
    print(WEBHOOK_URL, PORT)
    asyncio.run(main())
