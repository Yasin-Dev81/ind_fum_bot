from aiogram import Router, Dispatcher, F
from aiogram.types import CallbackQuery

from utils import MsgCB
from db.models import UserType
from filters import LimitLevel


router = Router(name="callbacks-router")
router.callback_query.filter(LimitLevel(type=UserType.SUPERUSER))


@router.callback_query(MsgCB.filter(F.action == "block"))
async def block(callback: CallbackQuery, callback_data: MsgCB):
    await callback.answer("comming soon ...", show_alert=True)


@router.callback_query(MsgCB.filter(F.action == "delete"))
async def delete(callback: CallbackQuery, callback_data: MsgCB):
    await callback.answer("comming soon ...", show_alert=True)


def register_callbacks(dp: Dispatcher):
    dp.include_router(router)
