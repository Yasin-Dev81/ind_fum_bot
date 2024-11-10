from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

# from db.methods2 import create_user
from db.methods import user_db


class DBCheck(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        event_from_user = data.get("event_from_user")
        if event_from_user:
            user = user_db.create(
                event_from_user.id,
                first_name=event_from_user.first_name,
                last_name=event_from_user.last_name,
                username=event_from_user.username or None,
            )
            data["user"] = user
        return await handler(event, data)
