from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import PAGINATION
from utils import MsgCB, MsgListCB, StarCB
from db.models import UserType, Message as MessageDB


def get_msg_list_inline_keyboard(
    msgs: list[MessageDB], page, type
) -> InlineKeyboardMarkup:
    start = page * PAGINATION
    end = start + PAGINATION
    paginated_msgs = msgs[start:end]

    builder = InlineKeyboardBuilder()
    for i in paginated_msgs:
        builder.row(
            InlineKeyboardButton(
                text=f"{i.title}",
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


def add_buttons(kb, row, buttons, pk):
    kb.insert(
        row,
        [
            InlineKeyboardButton(
                text=btn["text"],
                callback_data=MsgCB(pk=pk, action=btn["action"]).pack(),
            )
            for btn in buttons
        ],
    )


def get_msg_inline_keyboard(
    pk: int, user_type: UserType, done: bool = False, need_star: bool = False
) -> InlineKeyboardMarkup:
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
        add_buttons(
            kb,
            1,
            [
                {"text": "بلاک کردن ❌", "action": "block"},
                {"text": "حذف پیام 🗑", "action": "delete"},
            ],
            pk,
        )

        add_buttons(
            kb,
            0,
            [
                {"text": "تغییر وضعیت", "action": "update"},
                {"text": "✅" if done else "❎", "action": "update"},
            ],
            pk,
        )
        if need_star:
            add_buttons(kb, 1, [{"text": "تنظیم اولویت ⭐️", "action": "set_star"}], pk)

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


def get_star_inline_keyboard(pk: int) -> InlineKeyboardMarkup:
    kb = [
        [
            InlineKeyboardButton(
                text="1x⭐️", callback_data=StarCB(pk=pk, count=1).pack()
            ),
            InlineKeyboardButton(
                text="2x⭐️", callback_data=StarCB(pk=pk, count=2).pack()
            ),
        ],
        [
            InlineKeyboardButton(
                text="3x⭐️", callback_data=StarCB(pk=pk, count=3).pack()
            ),
            InlineKeyboardButton(
                text="4x⭐️", callback_data=StarCB(pk=pk, count=4).pack()
            ),
        ],
        [
            InlineKeyboardButton(
                text="5x⭐️", callback_data=StarCB(pk=pk, count=5).pack()
            ),
        ],
    ]
    return InlineKeyboardBuilder(kb).as_markup()
