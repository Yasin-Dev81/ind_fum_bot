from aiogram import Router, Dispatcher, F
from aiogram.types import CallbackQuery
from html import escape
from persiantools.jdatetime import JalaliDateTime

from utils import UserListCB, MsgCB, UserCB, StarCB
from keyboards import (
    get_user_list_inline_keyboard,
    get_user_inline_keyboard,
    get_msg_inline_keyboard,
    get_star_inline_keyboard,
)
from db.models import UserType
from db.methods import user_db, msg_db
from filters import LimitLevel
from config import DATE_TIME_FMT


router = Router(name="callbacks-router")
router.callback_query.filter(LimitLevel(type=UserType.ADMIN))


# ------------------------------------------------- msg
@router.callback_query(MsgCB.filter(F.action == "update"))
async def update_msg(callback: CallbackQuery, callback_data: MsgCB):
    # msg = msg_db.done(callback_data.pk)
    await callback.answer(
        "وضعیت به انجام شده تغییر کرد. ✅",
        show_alert=True,
    )
    await callback.message.edit_reply_markup(
        reply_markup=get_msg_inline_keyboard(
            callback_data.pk, UserType.ADMIN, done=True
        )
    )


@router.callback_query(MsgCB.filter(F.action == "set_star"))
async def set_star(callback: CallbackQuery, callback_data: MsgCB):
    await callback.message.answer(
        "چند ستاره مدنظرتان است:",
        reply_markup=get_star_inline_keyboard(callback_data.pk),
    )
    await callback.message.delete()


@router.callback_query(StarCB.filter())
async def set_star_count(callback: CallbackQuery, callback_data: StarCB):
    msg_db.set_star(callback_data.pk, callback_data.count)
    await callback.answer(
        f"{callback_data.count} ستاره با موفقیت ست شد.", show_alert=True
    )
    await callback.message.delete()

    msg = msg_db.msg(callback_data.pk)
    await callback.message.answer(
        (
            f"🆔 #{callback_data.pk}\n"
            f"👤 <b>{escape(msg.sender_name)}</b>\n"
            f"📅 <i>{JalaliDateTime(msg.datetime_created).strftime(DATE_TIME_FMT, locale='fa')}</i>\n"
            f"{(msg.star or 0) * '⭐️'}"
        ),
        reply_markup=get_msg_inline_keyboard(
            callback_data.pk,
            UserType.ADMIN,
            msg.done,
            not bool(msg.star or 0),
        ),
    )


# ------------------------------------------------- user
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
