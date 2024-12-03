from aiogram import Router, Dispatcher, F
from aiogram.types import Message

import aiostep

from db.models import UserType
from filters import LimitLevel


router = Router(name="devloper-messages-router")
router.message.filter(LimitLevel(type=UserType.DEVELOPER))


@router.message(F.text == "مدیا")
async def get_media_id(message: Message):
    await message.answer("مدیا را فروارد کنید:")
    try:
        response = await aiostep.wait_for(message.from_user.id, timeout=300)
        await message.answer("<code>%s</code>" % response.video.file_id)
    except TimeoutError:
        await message.answer("You took too long to answer.\nwe canceled this process!")
    except Exception as e:
        await message.answer(str(e))


def register_messages(dp: Dispatcher):
    dp.include_router(router)
