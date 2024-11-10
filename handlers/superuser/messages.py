from aiogram import Router, Dispatcher, F
from aiogram.types import Message

from db.models import UserType
from filters import LimitLevel


router = Router(name="messages-router")
router.message.filter(LimitLevel(type=UserType.SUPERUSER))


@router.message(F.text == "ارسال نوتیف")
async def send_notif(message: Message):
    await message.answer("comming soon ...")


@router.message(F.text == "سرچ")
async def search(message: Message):
    await message.answer("comming soon ...")


def register_messages(dp: Dispatcher):
    dp.include_router(router)
