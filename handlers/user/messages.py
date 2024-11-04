from aiogram import Router
from aiogram import Dispatcher


router = Router(name="messages-router")




def register_messages(dp: Dispatcher):
    dp.include_router(router)
