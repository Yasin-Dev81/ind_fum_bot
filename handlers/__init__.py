from aiogram import Dispatcher

from .user import register_callbacks, register_commands, register_messages
from .admin import register_admin_callbacks, register_messages_admin


def setup_routers(dp: Dispatcher):
    register_commands(dp)
    register_messages(dp)
    register_callbacks(dp)
    register_admin_callbacks(dp)
    register_messages_admin(dp)


__all__ = ("setup_routers",)
