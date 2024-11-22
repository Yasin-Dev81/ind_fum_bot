from aiogram.filters.callback_data import CallbackData
from typing import Optional


class MsgCB(CallbackData, prefix="msg"):
    pk: int
    action: str = "read"
    before_type: str = "all"


class StarCB(CallbackData, prefix="star"):
    pk: int
    count: int
    before_type: str = "all"


class StatusCB(CallbackData, prefix="star"):
    pk: int
    status_value: int
    before_type: str = "all"


class MsgListCB(CallbackData, prefix="list_msg"):
    page: int
    type: str = "unread"
    search_string: Optional[int] = None


class UserCB(CallbackData, prefix="user"):
    pk: int
    action: str = "read"


class UserListCB(CallbackData, prefix="list_user"):
    page: int
