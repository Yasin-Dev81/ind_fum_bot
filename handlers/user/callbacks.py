from aiogram import Router
from aiogram import Dispatcher


router = Router(name="callbacks-router")






def register_callbacks(dp: Dispatcher):
    dp.include_router(router)
