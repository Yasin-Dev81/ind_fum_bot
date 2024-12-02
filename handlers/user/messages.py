from aiogram import Router, Dispatcher, F
from aiogram.types import Message
from persiantools.jdatetime import JalaliDateTime

import re
import aiostep

from db.methods import msg_db
from keyboards import (
    get_msg_list_inline_keyboard,
    get_set_notif_file_id_inline_keyboard,
    get_cancel_inline_keyboard,
)
from db.models import UserType, User as UserModel
from filters import LimitLevel
from config import USER_LEVEL, DATE_TIME_FMT, RULES_MSG


router = Router(name="messages-router")
router.message.filter(LimitLevel(type=UserType.USER))


@router.message(F.text == "ارتباط با مدیر گروه 🚀")
async def send_superuser_msg(message: Message):
    await message.answer(
        (
            "لطفا پیام خود را بصورت متن ارسال کنید:\n"
            "در خط اول عنوان (حداکثر ۶۰ کارکتر) و در باقی خطوط پیام را بنویسید.\n\n"
            "- مثال:\n"
            "<blockquote expandable>عنوان تست\nمتن پیام تستی که میتونه هر چند خط که تلگرام اجازه میده باشه.</blockquote>"
        ),
        reply_markup=get_cancel_inline_keyboard(),
    )
    try:
        response: Message = await aiostep.wait_for(message.from_user.id, timeout=500)
        if response.text:
            match = re.match(r"^(^.{1,60})\n([\s\S]*)$", response.text)
            if match:
                msg_db.create(
                    title=match.group(1),
                    text=match.group(2),
                    sender_id=response.from_user.id,
                )

                await message.answer("پیام شما با موفقیت ثبت شد.")
            else:
                await message.answer(
                    "این ساختار متن مورد قبول نیست! (دوباره روی دکمه‌ی ارتباط با مدیر گروه بزنید)"
                )
        else:
            await message.answer(
                "صرفا متن ارسال کنید! (دوباره روی دکمه‌ی ارتباط با مدیر گروه بزنید)"
            )
    except TimeoutError:
        await message.answer("You took too long to answer.\nwe canceled this process!")
    except Exception:
        print(Exception)
        await message.answer("مشکلی پیش آمده است! لطفا دوباره تلاش کنید.")


@router.message(F.text == "پیام‌های خوانده نشده 📥")
async def unread_msg(message: Message):
    msgs = msg_db.uread_msgs(message.from_user.id)
    if not msgs:
        await message.answer("هیچ پیامی در لیست نیست!")
        return
    await message.answer(
        "یک پیام انتخاب کنید ⬇️",
        reply_markup=get_msg_list_inline_keyboard(msgs, page=0, type="unread"),
    )


@router.message(F.text == "تمامی پیام‌ها ↙️")
async def all_msg(message: Message):
    msgs = msg_db.all_msgs(message.from_user.id)
    if not msgs:
        await message.answer("هیچ پیامی در لیست نیست!")
        return
    await message.answer(
        "یک پیام انتخاب کنید ⬇️",
        reply_markup=get_msg_list_inline_keyboard(msgs, page=0, type="all"),
    )


@router.message(F.text == "پیام‌های ارسال شده ↗️")
async def sendes_msg(message: Message):
    msgs = msg_db.sendes_msgs(message.from_user.id)
    if not msgs:
        await message.answer("هیچ پیامی در لیست نیست!")
        return
    await message.answer(
        "یک پیام انتخاب کنید ⬇️",
        reply_markup=get_msg_list_inline_keyboard(msgs, page=0, type="sendes"),
    )


@router.message(F.text == "اطلاعات من ℹ️")
async def info(message: Message, user: UserModel):
    await message.answer(
        (
            f"🆔 #{user.id}\n"
            f"▫️ لول: {USER_LEVEL[user.type.value]}\n"
            f"◾️ نام مستعار: {user.nick_name or 'تعریف نشده!'}\n"
            f"▫️ زمان استارت بات: {JalaliDateTime(user.datetime_created).strftime(DATE_TIME_FMT, locale='fa')}"
        ),
        reply_markup=get_set_notif_file_id_inline_keyboard(),
    )


@router.message(F.text == "قوانین 📝")
async def rulles(message: Message, user: UserModel):
    await message.answer(RULES_MSG)


@router.message(F.text == "ارتباط با توسعه دهنده ⚠️")
async def send_admin_msg(message: Message):
    await message.answer(
        "لطفا پیام خود را ارسال کنید: (فقط متن)",
        reply_markup=get_cancel_inline_keyboard(),
    )
    try:
        response: Message = await aiostep.wait_for(message.from_user.id, timeout=300)

        if response.text:
            match = re.match(r"^(^.{1,60})\n([\s\S]*)$", response.text)
            if match:
                msg_db.create(
                    title=match.group(1),
                    text=match.group(2),
                    sender_id=response.from_user.id,
                    for_admin=False,
                )
                await message.answer("پیام شما با موفقیت ثبت شد.")
            else:
                msg_db.create(
                    title=None,
                    text=response.text,
                    sender_id=response.from_user.id,
                    for_admin=False,
                )
                await message.answer("پیام شما با موفقیت ثبت شد.")
        else:
            await message.answer(
                "صرفا متن ارسال کنید! (دوباره روی دکمه‌ی ارتباط با توسعه دهنده بزنید)"
            )
    except TimeoutError:
        await message.answer("You took too long to answer.\nwe canceled this process!")
    except Exception:
        print(Exception)
        await message.answer("مشکلی پیش آمده است! لطفا دوباره تلاش کنید.")


def register_messages(dp: Dispatcher):
    dp.include_router(router)
