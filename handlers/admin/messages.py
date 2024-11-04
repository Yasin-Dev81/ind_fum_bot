from aiogram import Router
from aiogram import Dispatcher

router = Router(name="messages-router")
router.message.filter(IsAdmin())



def register_messages_admin(dp: Dispatcher):
    dp.include_router(router)
