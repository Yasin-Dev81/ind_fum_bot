from aiogram import Dispatcher

from .user import register_callbacks, register_commands, register_messages
# from .superuser import superuser_register_callbacks, superuser_register_messages
from .admin import admin_register_callbacks, admin_register_messages
from .devloper import developer_register_messages

def setup_routers(dp: Dispatcher):
    register_commands(dp)
    register_messages(dp)
    register_callbacks(dp)
    # superuser_register_callbacks(dp)
    # superuser_register_messages(dp)
    admin_register_callbacks(dp)
    admin_register_messages(dp)
    developer_register_messages(dp)


__all__ = ("setup_routers",)
