from aiogram import Router, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from html import escape

import aiostep

from keyboards import get_main_menu_keyboard
from db.models import User as UserModel
from db.methods import user_db
from config import BOT_NAME


router = Router(name="commands-router")
# router.message.filter(LimitLevel(type=UserType.USER))


@router.message(Command("start"))
async def start(message: Message, user: UserModel):
    if not user.nick_name:
        await message.answer("لطفا نام خود را ارسال کنید:")
        try:
            response: Message = await aiostep.wait_for(
                message.from_user.id, timeout=500
            )

            if response.text:
                user_db.set_name(user.id, response.text[:128])

                await message.answer("نام شما با موفقیت ثبت شد ✅")
                await message.answer(
                    f"سلام {escape(response.text)}\n به بات {BOT_NAME} خوش اومدی 👋🏻",
                    reply_markup=get_main_menu_keyboard(user.type.value),
                )
            else:
                await message.answer("صرفا متن ارسال کنید! (دوباره روی /start بزنید)")
        except TimeoutError:
            await message.answer(
                "You took too long to answer.\nwe canceled this process!\n"
                "(دوباره روی /start بزنید)"
            )
        except Exception:
            print(Exception)
            await message.answer("مشکلی پیش آمده است! لطفا دوباره تلاش کنید.")
    else:
        await message.answer(
            f"سلام {escape(user.name)}\n به بات {BOT_NAME} خوش اومدی 👋🏻",
            reply_markup=get_main_menu_keyboard(user.type.value),
        )
    await message.answer("Powered by @MmdYasin02")


def register_commands(dp: Dispatcher):
    dp.include_router(router)
