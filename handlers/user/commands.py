from aiogram import Router, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message


router = Router(name="commands-router")


@router.message(Command("start"))
async def start(message: Message, command):
    pass


def register_commands(dp: Dispatcher):
    dp.include_router(router)
