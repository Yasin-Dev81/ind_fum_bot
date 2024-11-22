from aiogram import Router, Dispatcher, F
from aiogram.types import CallbackQuery
from html import escape
from persiantools.jdatetime import JalaliDateTime

# import asyncio

from utils import UserListCB, MsgCB, UserCB, StarCB, StatusCB
from keyboards import (
    get_user_list_inline_keyboard,
    get_user_inline_keyboard,
    get_msg_inline_keyboard,
    get_star_inline_keyboard,
    get_status_type_inline_keyboard,
)
from db.models import UserType
from db.methods import user_db, msg_db
from filters import LimitLevel
from config import DATE_TIME_FMT, STATUS_LEVEL
import glv


router = Router(name="callbacks-router")
router.callback_query.filter(LimitLevel(type=UserType.ADMIN))


# ------------------------------------------------- msg
@router.callback_query(MsgCB.filter(F.action == "update"))
async def update_msg(callback: CallbackQuery, callback_data: MsgCB):
    await callback.answer("وضعیت را مشخص کنید.")
    await callback.message.answer(
        "وضعیت را مشخص کنید ⬇️",
        reply_markup=get_status_type_inline_keyboard(callback_data.pk),
    )


@router.callback_query(StatusCB.filter())
async def set_status_msg(callback: CallbackQuery, callback_data: StatusCB):
    msg_db.update_status(callback_data.pk, callback_data.status_value)
    await callback.answer(
        f"وضعیت {STATUS_LEVEL[callback_data.status_value]} تنظیم شد.", show_alert=True
    )
    await callback.message.delete()


@router.callback_query(MsgCB.filter(F.action == "set_star"))
async def set_star(callback: CallbackQuery, callback_data: MsgCB):
    await callback.message.answer(
        "چند ستاره مدنظرتان است ⬇️",
        reply_markup=get_star_inline_keyboard(callback_data.pk),
    )
    # await callback.message.delete()


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


@router.callback_query(MsgCB.filter(F.action == "delete"))
async def delete_msg(callback: CallbackQuery, callback_data: MsgCB):
    msg_db.delete(callback_data.pk)
    await callback.answer(
        "پیام با موفقیت حذف شد. 🗑",
        show_alert=True,
    )
    await callback.message.delete()


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
        f"🆔 #{callback_data.pk}\n👤 {escape(user.name)}\n💬 @{user.username}\n"
        f"📅 {JalaliDateTime(user.datetime_created).strftime(DATE_TIME_FMT, locale='fa')}",
        reply_markup=get_user_inline_keyboard(callback_data.pk, user.type.value),
    )
    await callback.message.delete()


@router.callback_query(UserCB.filter(F.action == "set_superuser"))
async def set_superuser(callback: CallbackQuery, callback_data: MsgCB):
    user_db.set_superuser(callback_data.pk)
    await callback.answer("با موفقیت سوپر یوزر شد.", show_alert=True)
    await callback.message.edit_reply_markup(
        reply_markup=get_user_inline_keyboard(callback_data.pk, 2),
    )
    await glv.bot.send_message(
        callback_data.pk, "تبریک 🎉\nشما به واسطه‌ی مدیر گروه <b>سوپریوزر</b> شدید."
    )


def register_callbacks(dp: Dispatcher):
    dp.include_router(router)
