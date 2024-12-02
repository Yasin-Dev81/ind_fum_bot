from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_cancel_inline_keyboard() -> InlineKeyboardMarkup:
    kb = [
        [
            InlineKeyboardButton(
                text="✖️ cancel", callback_data="exit"
            )
        ],
    ]
    return InlineKeyboardBuilder(kb).as_markup()
