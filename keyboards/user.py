from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import PAGINATION
from utils import UserCB, UserListCB


def get_user_list_inline_keyboard(msgs, page) -> InlineKeyboardMarkup:
    start = page * PAGINATION
    end = start + PAGINATION
    paginated_msgs = msgs[start:end]

    builder = InlineKeyboardBuilder()
    for i in paginated_msgs:
        builder.row(
            InlineKeyboardButton(
                text=i.name,
                callback_data=UserCB(pk=i.id).pack(),
            )
        )

    navigation_buttons = []
    if start > 0:
        navigation_buttons.append(
            InlineKeyboardButton(
                text="◀️ Previous",
                callback_data=UserListCB(page=page - 1).pack(),
            )
        )
    if end < len(msgs):
        navigation_buttons.append(
            InlineKeyboardButton(
                text="Next ▶️",
                callback_data=UserListCB(page=page + 1).pack(),
            )
        )

    if navigation_buttons:
        builder.row(*navigation_buttons)

    builder.row(
        InlineKeyboardButton(text="بازگشت 🔙", callback_data="exit"),
        InlineKeyboardButton(text="خروج ✖️", callback_data="exit"),
    )
    return builder.as_markup()


def get_user_inline_keyboard(pk: int, type_value: int) -> InlineKeyboardMarkup:
    kb = [
        [
            InlineKeyboardButton(
                text="بلاک کردن ❌",
                callback_data=UserCB(pk=pk, action="block").pack(),
            ),
            InlineKeyboardButton(
                text="حذف پیام 🗑",
                callback_data=UserCB(pk=pk, action="delete").pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text="بازگشت 🔙", callback_data=UserListCB(page=0).pack()
            ),
            InlineKeyboardButton(text="خروج ✖️", callback_data="exit"),
        ],
    ]
    if type_value == 3:
        kb.insert(
            0,
            [
                InlineKeyboardButton(
                    text="set superuser",
                    callback_data=UserCB(pk=pk, action="set_superuser").pack(),
                )
            ],
        )
    return InlineKeyboardBuilder(kb).as_markup()


def get_notif_user_inline_keyboard(pk: int) -> InlineKeyboardMarkup:
    kb = [
        [
            InlineKeyboardButton(
                text="مشاهده", callback_data=UserCB(pk=pk, action="read").pack()
            )
        ],
    ]
    return InlineKeyboardBuilder(kb).as_markup()
