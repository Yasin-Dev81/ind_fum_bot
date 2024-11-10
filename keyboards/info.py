from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_set_notif_file_id_inline_keyboard() -> InlineKeyboardMarkup:
    kb = [
        [
            InlineKeyboardButton(
                text="تنظیم ویس نوتیف", callback_data="set_notif_file_id"
            )
        ],
    ]
    return InlineKeyboardBuilder(kb).as_markup()
