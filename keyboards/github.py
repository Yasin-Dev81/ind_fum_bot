from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import GITHUB_LINK


def get_github_inline_keyboard() -> InlineKeyboardMarkup:
    kb = [
        [
            InlineKeyboardButton(
                text="source code (github)",
                url=GITHUB_LINK,
            )
        ],
    ]
    return InlineKeyboardBuilder(kb).as_markup()
