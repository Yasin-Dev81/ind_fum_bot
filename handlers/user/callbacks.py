from aiogram import Router, Dispatcher, F
from aiogram.types import CallbackQuery, Message
from html import escape
from persiantools.jdatetime import JalaliDateTime
import aiostep
import asyncio
import re

from utils import MsgListCB, MsgCB
from keyboards import get_msg_list_inline_keyboard, get_msg_inline_keyboard
from db.methods import msg_db, user_db
from config import DATE_TIME_FMT
# from db.models import UserType
# from filters import LimitLevel


router = Router(name="callbacks-router")
# router.callback_query.filter(LimitLevel(type=UserType.USER))


@router.callback_query(MsgListCB.filter())
async def list_msg(callback: CallbackQuery, callback_data: MsgListCB):
    msgs = msg_db.uread_msgs(callback.from_user.id)
    await callback.message.edit_reply_markup(
        reply_markup=get_msg_list_inline_keyboard(
            msgs, page=callback_data.page, type=callback_data.type
        )
    )


# @router.callback_query(MsgListCB.filter(F.type == "all"))
# async def all_msgs(callback: CallbackQuery, callback_data: MsgListCB):
#     msgs = msg_db.all_msgs(callback.from_user.id)
#     await callback.message.edit_reply_markup(
#         reply_markup=get_msg_list_inline_keyboard(
#             msgs, page=callback_data.page, type="all"
#         )
#     )


@router.callback_query(MsgCB.filter(F.action == "read"))
async def msg(callback: CallbackQuery, callback_data: MsgCB):
    msg = msg_db.msg(callback_data.pk)
    user = user_db.read(callback.from_user.id)
    await callback.message.answer(
        (
            f"📌 {escape(msg.title) or 'بدون عنوان'}\n"
            f"<blockquote expandable>{escape(msg.caption)}</blockquote>"
        ),
    )
    await callback.message.answer(
        (
            f"🆔 #{callback_data.pk}\n"
            f"⚡️ superuser: {'✅'if msg.is_superuser else '❎'}\n"
            f"👤 name: <b>{escape(msg.sender_name)}</b>\n"
            f"📅 <i>{JalaliDateTime(msg.datetime_created).strftime(DATE_TIME_FMT, locale='fa')}</i>\n"
            f"{(msg.star or 0) * '⭐️'}"
        ),
        reply_markup=get_msg_inline_keyboard(
            callback_data.pk,
            user.type,
            msg.done,
            not bool(msg.star or 0),
        ),
    )
    await callback.message.delete()
    asyncio.create_task(msg_db.seen(callback_data.pk))


@router.callback_query(MsgCB.filter(F.action == "reply"))
async def reply(callback: CallbackQuery, callback_data: MsgCB):
    await callback.message.answer(
        "لطفا پیام خود را ارسال کنید: (فقط متن)", show_alert=True
    )
    try:
        response: Message = await aiostep.wait_for(callback.from_user.id, timeout=500)
        if response.text:
            match = re.match(r"^(^.{1,60})\n([\s\S]*)$", response.text)
            if match:
                msg_db.reply(
                    title=match.group(1),
                    text=match.group(2),
                    sender_id=response.from_user.id,
                    msg_id=callback_data.pk,
                )
                await callback.message.answer("پیام شما با موفقیت ثبت شد.")
            else:
                msg_db.reply(
                    title=None,
                    text=response.text,
                    sender_id=response.from_user.id,
                    msg_id=callback_data.pk,
                )
                await callback.message.answer("پیام شما با موفقیت ثبت شد.")
        else:
            await callback.message.answer(
                "صرفا متن ارسال کنید! (دوباره روی دکمه‌ی پاسخ بزنید)"
            )
        await callback.message.delete()
    except TimeoutError:
        await callback.message.answer(
            "You took too long to answer.\nwe canceled this process!"
        )
    except Exception:
        print(Exception)
        await callback.message.answer("مشکلی پیش آمده است! لطفا دوباره تلاش کنید.")


@router.callback_query(F.data == "set_notif_file_id")
async def set_notif_file_id(callback: CallbackQuery):
    await callback.answer("لطفا ویس خود را ارسال کنید:", show_alert=True)
    try:
        response: Message = await aiostep.wait_for(callback.from_user.id, timeout=500)
        if response.voice:
            user_db.set_notif_file_id(callback.from_user.id, response.voice.file_id)

            await callback.message.answer("ویس شما با موفقیت ذخیره شد.")
        else:
            await callback.message.answer(
                "صرفا ویس ارسال کنید! (دوباره روی دکمه‌ی پاسخ بزنید)"
            )
        await callback.message.delete()
    except TimeoutError:
        await callback.message.answer(
            "You took too long to answer.\nwe canceled this process!"
        )
    except Exception:
        print(Exception)
        await callback.message.answer("مشکلی پیش آمده است! لطفا دوباره تلاش کنید.")


def register_callbacks(dp: Dispatcher):
    dp.include_router(router)
