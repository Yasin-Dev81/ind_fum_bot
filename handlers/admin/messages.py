from aiogram import Router, Dispatcher, F
from aiogram.types import Message

from db.methods import user_db, msg_db
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


@router.message(F.text == "موضوعات انجام نشده ❎")
async def unread_msg(message: Message):
    msgs = msg_db.udone_msgs(message.from_user.id)
    await message.answer(
        "یک پیام انتخاب کنید:",
        reply_markup=get_msg_list_inline_keyboard(msgs, page=0, type="udone"),
    )


@router.message(F.text == "سرچ 🔎")
async def search(message: Message):
    await message.answer("comming soon ...")


@router.message(F.text == "ارسال نوتیف 🔊")
async def send_notif(message: Message):
    await message.answer("comming soon ...")


@router.message(F.text == "گزارش عملکرد 📈")
async def report(message: Message):
    await message.answer("comming soon ...")


def register_messages(dp: Dispatcher):
    dp.include_router(router)
