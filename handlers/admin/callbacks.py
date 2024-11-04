from aiogram import Router
from aiogram import Dispatcher
from filters import IsAdmin

router = Router(name="admin-callbacks-router")
router.callback_query.filter(IsAdmin())



def register_admin_callbacks(dp: Dispatcher):
    dp.include_router(router)
