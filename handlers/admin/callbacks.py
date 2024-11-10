from aiogram import Router, Dispatcher, F
from aiogram.types import CallbackQuery
from html import escape

from utils import UserListCB, MsgCB, UserCB
from keyboards import get_user_list_inline_keyboard, get_user_inline_keyboard
from db.models import UserType
from db.methods import user_db
from filters import LimitLevel


router = Router(name="callbacks-router")
router.callback_query.filter(LimitLevel(type=UserType.ADMIN))


@router.callback_query(UserListCB.filter())
async def list_user(callback: CallbackQuery, callback_data: UserListCB):
    users = user_db.read_alls()
    await callback.message.edit_reply_markup(
        reply_markup=get_user_list_inline_keyboard(users, callback_data.page)
    )


@router.callback_query(UserCB.filter(F.action == "read"))
async def user(callback: CallbackQuery, callback_data: MsgCB):
    user = user_db.read(callback_data.pk)
    await callback.message.answer(
        f"🆔 #{callback_data.pk}\n👤 {escape(user.name)}\n💬 @{user.username}",
        reply_markup=get_user_inline_keyboard(callback_data.pk, user.type.value),
    )
    await callback.message.delete()


@router.callback_query(UserCB.filter(F.action == "set_superuser"))
async def set_superuser(callback: CallbackQuery, callback_data: MsgCB):
    user_db.set_superuser(callback_data.pk)
    await callback.answer("با موفقیت سوپر یوزر شد.", show_alert=True)
    await callback.message.edit_reply_markup(
        reply_markup=get_user_inline_keyboard(callback_data.pk, 1),
    )


def register_callbacks(dp: Dispatcher):
    dp.include_router(router)
