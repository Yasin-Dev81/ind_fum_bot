from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import PAGINATION
from utils import MsgCB, MsgListCB
from db.models import UserType


def get_msg_list_inline_keyboard(msgs, page, type) -> InlineKeyboardMarkup:
    start = page * PAGINATION
    end = start + PAGINATION
    paginated_msgs = msgs[start:end]

    builder = InlineKeyboardBuilder()
    for i in paginated_msgs:
        builder.row(
            InlineKeyboardButton(
                text=f"#{i.id}",
                callback_data=MsgCB(pk=i.id).pack(),
            )
        )

    navigation_buttons = []
    if start > 0:
        navigation_buttons.append(
            InlineKeyboardButton(
                text="◀️ Previous",
                callback_data=MsgListCB(page=page - 1, type=type).pack(),
            )
        )
    if end < len(msgs):
        navigation_buttons.append(
            InlineKeyboardButton(
                text="Next ▶️",
                callback_data=MsgListCB(page=page + 1, type=type).pack(),
            )
        )

    if navigation_buttons:
        builder.row(*navigation_buttons)

    builder.row(
        InlineKeyboardButton(text="بازگشت 🔙", callback_data="exit"),
        InlineKeyboardButton(text="خروج ✖️", callback_data="exit"),
    )
    return builder.as_markup()


def get_msg_inline_keyboard(pk: int, user_type: UserType) -> InlineKeyboardMarkup:
    kb = [
        [
            InlineKeyboardButton(
                text="پاسخ دادن", callback_data=MsgCB(pk=pk, action="reply").pack()
            )
        ],
        [
            InlineKeyboardButton(
                text="بازگشت 🔙", callback_data=MsgListCB(page=0).pack()
            ),
            InlineKeyboardButton(text="خروج ✖️", callback_data="exit"),
        ],
    ]
    if user_type in [UserType.ADMIN, UserType.SUPERUSER]:
        kb.insert(
            1,
            [
                InlineKeyboardButton(
                    text="بلاک کردن ❌",
                    callback_data=MsgCB(pk=pk, action="block").pack(),
                ),
                InlineKeyboardButton(
                    text="حذف پیام 🗑",
                    callback_data=MsgCB(pk=pk, action="delete").pack(),
                ),
            ],
        )
    return InlineKeyboardBuilder(kb).as_markup()


def get_notif_inline_keyboard(pk: int) -> InlineKeyboardMarkup:
    kb = [
        [
            InlineKeyboardButton(
                text="مشاهده", callback_data=MsgCB(pk=pk, action="read").pack()
            )
        ],
    ]
    return InlineKeyboardBuilder(kb).as_markup()
