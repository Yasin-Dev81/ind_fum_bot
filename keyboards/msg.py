from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import PAGINATION, STATUS_LEVEL
from utils import MsgCB, MsgListCB, StarCB, StatusCB
from db.models import UserType, Message as MessageDB


def get_msg_list_inline_keyboard(
    msgs: list[MessageDB], page, type, search_string = None
) -> InlineKeyboardMarkup:
    start = page * PAGINATION
    end = start + PAGINATION
    paginated_msgs = msgs[start:end]

    builder = InlineKeyboardBuilder()
    for i in paginated_msgs:
        builder.row(
            InlineKeyboardButton(
                text="{status} {title}".format(
                    status="✅" if i.done else "❎",
                    title=(
                        (i.title[:20] + "...")
                        if i.title and len(i.title) > 20
                        else (i.title or "بدون عنوان")
                    ),
                ),
                callback_data=MsgCB(pk=i.id, before_type=type).pack(),
            )
        )

    navigation_buttons = []
    if start > 0:
        navigation_buttons.append(
            InlineKeyboardButton(
                text="◀️ Previous",
                callback_data=MsgListCB(page=page - 1, type=type, search_string=search_string).pack(),
            )
        )
    if end < len(msgs):
        navigation_buttons.append(
            InlineKeyboardButton(
                text="Next ▶️",
                callback_data=MsgListCB(page=page + 1, type=type, search_string=search_string).pack(),
            )
        )

    if navigation_buttons:
        builder.row(*navigation_buttons)

    builder.row(
        InlineKeyboardButton(text="بازگشت 🔙", callback_data="exit"),
        InlineKeyboardButton(text="خروج ✖️", callback_data="exit"),
    )
    return builder.as_markup()


def add_buttons(kb, row, buttons, pk, before_type="all"):
    kb.insert(
        row,
        [
            InlineKeyboardButton(
                text=btn["text"],
                callback_data=MsgCB(
                    pk=pk, action=btn["action"], before_type=before_type
                ).pack(),
            )
            for btn in buttons
        ],
    )


def get_msg_inline_keyboard(
    pk: int,
    user_type: UserType,
    need_star: bool = False,
    before_type: str = "all",
) -> InlineKeyboardMarkup:
    kb = [
        [
            InlineKeyboardButton(
                text="پاسخ دادن", callback_data=MsgCB(pk=pk, action="reply").pack()
            )
        ],
        [
            InlineKeyboardButton(
                text="بازگشت 🔙",
                callback_data=MsgListCB(page=0, type=before_type).pack(),
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
            ],
            pk,
            before_type,
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
        [
            InlineKeyboardButton(text="cancel", callback_data="exit"),
        ],
    ]
    return InlineKeyboardBuilder(kb).as_markup()


def get_status_type_inline_keyboard(pk: int) -> InlineKeyboardMarkup:
    kb = [
        [
            InlineKeyboardButton(
                text=STATUS_LEVEL[i],
                callback_data=StatusCB(pk=pk, status_value=i).pack(),
            ),
        ]
        for i in range(4)
    ] + [
        [
            InlineKeyboardButton(text="cancel", callback_data="exit"),
        ],
    ]
    return InlineKeyboardBuilder(kb).as_markup()
