from aiogram import Router, Dispatcher, F
from aiogram.types import Message

import aiostep
import asyncio

from db.methods import user_db, msg_db, report_db
from utils import send_msg_list
from keyboards import get_user_list_inline_keyboard, get_msg_list_inline_keyboard
from db.models import UserType
from filters import LimitLevel


router = Router(name="messages-router")
router.message.filter(LimitLevel(type=UserType.ADMIN))


@router.message(F.text == "یوزرها 👥")
async def users(message: Message):
    users = user_db.read_alls()
    await message.answer(
        "یک یوزر انتخاب کنید:", reply_markup=get_user_list_inline_keyboard(users, 0)
    )


@router.message(F.text == "انجام نشده ❎")
async def udone_msg(message: Message):
    msgs = msg_db.inqueue_msgs(message.from_user.id)
    if not msgs:
        await message.answer("هیچ پیامی در لیست نیست!")
        return
    await message.answer(
        "یک پیام انتخاب کنید ⬇️",
        reply_markup=get_msg_list_inline_keyboard(msgs, page=0, type="udone"),
    )


@router.message(F.text == "در حال انجام 🔄")
async def process_msg(message: Message):
    msgs = msg_db.process_msgs(message.from_user.id)
    if not msgs:
        await message.answer("هیچ پیامی در لیست نیست!")
        return
    await message.answer(
        "یک پیام انتخاب کنید ⬇️",
        reply_markup=get_msg_list_inline_keyboard(msgs, page=0, type="process"),
    )


@router.message(F.text == "سرچ 🔎")
async def search(message: Message):
    await message.answer("لطفا عنوان مدنظر را ارسال کنید:")
    try:
        response: Message = await aiostep.wait_for(message.from_user.id, timeout=500)

        if response.text:
            msgs = msg_db.search(response.text)

            await response.answer(
                "یک پیام انتخاب کنید ⬇️",
                reply_markup=get_msg_list_inline_keyboard(
                    msgs, page=0, type="search", search_string=response.text
                ),
            )
        else:
            await message.answer("صرفا متن ارسال کنید! (دوباره روی تلاش کنید)")
    except TimeoutError:
        await message.answer("You took too long to answer.\nwe canceled this process!")
    except Exception:
        print(Exception)
        await message.answer("مشکلی پیش آمده است! لطفا دوباره تلاش کنید.")


@router.message(F.text == "ارسال نوتیف 🔊")
async def send_notif(message: Message):
    await message.answer("لطفا متن مدنظر را ارسال کنید:")
    try:
        response: Message = await aiostep.wait_for(message.from_user.id, timeout=1000)

        if response.text:
            asyncio.create_task(
                send_msg_list(
                    user_db.read_alls(),
                    f"🔊 <tg-spoiler>اعلان از طرف مدیر گروه</tg-spoiler>\n{response.text}",
                    response.from_user.id,
                )
            )

            await message.answer("پیام در صف ارسال قرار گرفت.")
        else:
            await message.answer("صرفا متن ارسال کنید! (دوباره روی تلاش کنید)")
    except TimeoutError:
        await message.answer("You took too long to answer.\nwe canceled this process!")
    except Exception:
        print(Exception)
        await message.answer("مشکلی پیش آمده است! لطفا دوباره تلاش کنید.")


@router.message(F.text == "گزارش عملکرد 📈")
async def report(message: Message):
    await message.answer(str(report_db.user_count()))
    await message.answer(str(report_db.user_count(True)))
    await message.answer(str(report_db.get_top_starred_messages()))


def register_messages(dp: Dispatcher):
    dp.include_router(router)
