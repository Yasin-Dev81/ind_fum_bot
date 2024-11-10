from aiogram import Router, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from html import escape

from keyboards import get_main_menu_keyboard
from db.models import User as UserModel


router = Router(name="commands-router")
# router.message.filter(LimitLevel(type=UserType.USER))


@router.message(Command("start"))
async def start(message: Message, user: UserModel):
    await message.answer(
        f"سلام {escape(message.from_user.first_name)}\n به نسخه‌ی بدون نام بات خوش اومدی 👋🏻",
        reply_markup=get_main_menu_keyboard(user.type.value),
    )
    await message.answer("Powered by @MmdYasin02")


def register_commands(dp: Dispatcher):
    dp.include_router(router)
