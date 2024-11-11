from aiogram import Router, Dispatcher#, F
# from aiogram.types import CallbackQuery

# from utils import MsgCB
# from db.models import UserType
# from filters import LimitLevel


router = Router(name="callbacks-router")
# router.callback_query.filter(LimitLevel(type=UserType.SUPERUSER))



def register_callbacks(dp: Dispatcher):
    dp.include_router(router)
