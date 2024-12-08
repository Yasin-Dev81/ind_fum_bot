from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_cancel_inline_keyboard(cancel_name=False) -> InlineKeyboardMarkup:
    kb = [
        [
            InlineKeyboardButton(
                text="✖️ cancel",
                callback_data="exit" if not cancel_name else "cancel_name",
            )
        ],
    ]
    return InlineKeyboardBuilder(kb).as_markup()
