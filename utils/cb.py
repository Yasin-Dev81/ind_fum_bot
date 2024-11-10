from aiogram.filters.callback_data import CallbackData


class MsgCB(CallbackData, prefix="msg"):
    pk: int
    action: str = "read"


class MsgListCB(CallbackData, prefix="list_msg"):
    page: int
    type: str = "unread"


class UserCB(CallbackData, prefix="user"):
    pk: int
    action: str = "read"


class UserListCB(CallbackData, prefix="list_user"):
    page: int
