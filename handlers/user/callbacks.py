from aiogram import Router, Dispatcher, F
from aiogram.types import CallbackQuery, Message
from html import escape
from persiantools.jdatetime import JalaliDateTime
import aiostep
import asyncio
import re

from utils import MsgListCB, MsgCB
from keyboards import (
    get_msg_list_inline_keyboard,
    get_msg_inline_keyboard,
    get_cancel_inline_keyboard,
    get_main_menu_keyboard,
)
from db.methods import msg_db, user_db
from config import DATE_TIME_FMT, STATUS_LEVEL, LEARN_VIDEO_URL, BOT_NAME
# from db.models import UserType
# from filters import LimitLevel


router = Router(name="callbacks-router")
# router.callback_query.filter(LimitLevel(type=UserType.USER))


@router.callback_query(F.data == "exit")
async def exit(callback: CallbackQuery):
    await aiostep.unregister_steps(callback.from_user.id)
    await callback.message.answer_video(
        video=LEARN_VIDEO_URL,
        caption=(
            f"سلام دوست من\n به بات {BOT_NAME} خوش اومدی 👋🏻\n\n"
            "یه ویدیو برای نحوه‌ی استفاده از بات آماده کردیم، اگه دوست داشتی قبل از استفاده ویدیو رو ببین.\n"
            "راستی اگه موقع استفاده از بات به مشکلی برخوردی حتما بهم بگو 🙏"
        ),
        reply_markup=get_main_menu_keyboard(user.type.value),
    )
    await callback.message.answer("Powered by <span class='tg-spoiler'>@MmdYasin02</span>")
    await callback.message.delete()


@router.callback_query(F.data == "cancel_name")
async def cancel_name(callback: CallbackQuery):
    await aiostep.unregister_steps(callback.from_user.id)
    await callback.message.answer_video(
        video=LEARN_VIDEO_URL,
        caption=(
            f"سلام دوست من\n به بات {BOT_NAME} خوش اومدی 👋🏻\n\n"
            "یه ویدیو برای نحوه‌ی استفاده از بات آماده کردیم، اگه دوست داشتی قبل از استفاده ویدیو رو ببین.\n"
            "راستی اگه موقع استفاده از بات به مشکلی برخوردی حتما بهم بگو 🙏"
        ),
        reply_markup=get_main_menu_keyboard(3),
    )
    await callback.message.answer("Powered by <span class='tg-spoiler'>@MmdYasin02</span>")
    await callback.message.delete()


@router.callback_query(MsgListCB.filter())
async def list_msg(callback: CallbackQuery, callback_data: MsgListCB):
    if callback_data.type == "unread":
        msgs = msg_db.uread_msgs(callback.from_user.id, callback_data.page + 1)
    elif callback_data.type == "udone":
        msgs = msg_db.inqueue_msgs(callback.from_user.id, callback_data.page + 1)
    elif callback_data.type == "process":
        msgs = msg_db.process_msgs(callback.from_user.id, callback_data.page + 1)
    elif callback_data.type == "sendes":
        msgs = msg_db.sendes_msgs(callback.from_user.id, callback_data.page + 1)
    elif callback_data.type == "search":
        msgs = msg_db.search(callback_data.search_string)
    else:
        msgs = msg_db.all_msgs(callback.from_user.id, callback_data.page)

    if callback_data.page == 0:
        await callback.message.answer(
            "یک پیام انتخاب کنید ⬇️",
            reply_markup=get_msg_list_inline_keyboard(
                msgs,
                page=0,
                type=callback_data.type,
                search_string=callback_data.search_string,
            ),
        )
        await callback.message.delete()
    else:
        await callback.message.edit_reply_markup(
            reply_markup=get_msg_list_inline_keyboard(
                msgs,
                page=callback_data.page,
                type=callback_data.type,
                search_string=callback_data.search_string,
            )
        )


@router.callback_query(MsgCB.filter(F.action == "read"))
async def msg(callback: CallbackQuery, callback_data: MsgCB):
    msg = msg_db.msg(callback_data.pk)
    user = user_db.read(callback.from_user.id)
    superuser_status = (
        f"⚡️ superuser: {'✅'if msg.is_superuser else '❎'}\n"
        if user.type.value <= 1
        else ""
    )
    await callback.message.answer(msg.tel_msg)
    await callback.message.answer(
        (
            f"🆔 #{callback_data.pk}\n{superuser_status}"
            f"◾️ وضعیت: <b>{STATUS_LEVEL[msg.status.value]}</b>\n"
            f"👤 فرستنده: <b>{escape(msg.sender_name)}</b> {msg.xname if user.type.value <= 1 else ''}\n"
            f"📅 زمان ارسال: <i>{JalaliDateTime(msg.datetime_created).strftime(DATE_TIME_FMT, locale='fa')}</i>\n"
            f"{(msg.star or 0) * '⭐️'}"
        ),
        reply_markup=get_msg_inline_keyboard(
            callback_data.pk,
            user.type,
            not (bool(msg.star or 0)),
            before_type=callback_data.before_type,
        ),
    )
    await callback.message.delete()
    asyncio.create_task(msg_db.seen(callback_data.pk))


@router.callback_query(MsgCB.filter(F.action == "reply"))
async def reply(callback: CallbackQuery, callback_data: MsgCB):
    await callback.message.answer(
        "لطفا پیام خود را ارسال کنید: (فقط متن)",
        reply_markup=get_cancel_inline_keyboard(),
    )
    try:
        response: Message = await aiostep.wait_for(callback.from_user.id, timeout=500)
        if response.text:
            match = re.match(r"^(^.{1,60})\n([\s\S]*)$", response.text + "\n")
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
