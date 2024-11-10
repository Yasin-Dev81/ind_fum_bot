from aiogram import Router, Dispatcher, F
from aiogram.types import Message

from db.methods import user_db
from keyboards import get_user_list_inline_keyboard
from db.models import UserType
from filters import LimitLevel


router = Router(name="messages-router")
router.message.filter(LimitLevel(type=UserType.ADMIN))


@router.message(F.text == "یوزرها")
async def users(message: Message):
    users = user_db.read_alls()
    await message.answer(
        "یک یوزر انتخاب کنید:", reply_markup=get_user_list_inline_keyboard(users, 0)
    )


def register_messages(dp: Dispatcher):
    dp.include_router(router)
