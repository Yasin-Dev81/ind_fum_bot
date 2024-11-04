from aiogram.filters import Filter
from db.methods import user_db


class IsAdmin(Filter):
    async def __call__(self, update: any, **data) -> bool:
        user = data["event_from_user"]
        return user_db.is_admin(user.id)
