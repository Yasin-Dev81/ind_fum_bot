from aiogram import Router, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from html import escape

import aiostep

from keyboards import (
    get_main_menu_keyboard,
    get_cancel_inline_keyboard,
    get_github_inline_keyboard,
)
from db.models import User as UserModel
from db.methods import user_db
from config import BOT_NAME, LEARN_VIDEO_URL


router = Router(name="commands-router")
# router.message.filter(LimitLevel(type=UserType.USER))


@router.message(Command("start"))
async def start(message: Message, user: UserModel):
    if not user.nick_name:
        await message.answer(
            "در صورت تمایل می‌توانید یک نام مستعار برای خودتون تعیین کنید:",
            reply_markup=get_cancel_inline_keyboard(cancel_name=True),
        )
        try:
            response: Message = await aiostep.wait_for(
                message.from_user.id, timeout=600
            )

            if response.text:
                user_db.set_name(user.id, response.text[:128])

                await message.answer("نام شما با موفقیت ثبت شد ✅")
                await message.answer_video(
                    video=LEARN_VIDEO_URL,
                    caption=(
                        f"سلام {escape(user.name)}\n به بات {BOT_NAME} خوش اومدی 👋🏻\n\n"
                        "یه ویدیو برای نحوه‌ی استفاده از بات آماده کردیم، اگه دوست داشتی قبل از استفاده ویدیو رو ببین.\n"
                        "راستی اگه موقع استفاده از بات به مشکلی برخوردی حتما بهم بگو 🙏"
                    ),
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
        await message.answer_video(
            video=LEARN_VIDEO_URL,
            caption=(
                f"سلام {escape(user.name)}\n به بات {BOT_NAME} خوش اومدی 👋🏻\n\n"
                "یه ویدیو برای نحوه‌ی استفاده از بات آماده کردیم، اگه دوست داشتی قبل از استفاده ویدیو رو ببین.\n"
                "راستی اگه موقع استفاده از بات به مشکلی برخوردی حتما بهم بگو 🙏"
            ),
            reply_markup=get_main_menu_keyboard(user.type.value),
        )
    await message.answer(
        "Powered by <span class='tg-spoiler'>@MmdYasin02</span>",
        reply_markup=get_github_inline_keyboard(),
    )


def register_commands(dp: Dispatcher):
    dp.include_router(router)
