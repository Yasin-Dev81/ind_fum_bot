from aiogram.filters import Filter
from db.models import UserType, User as UserModel


class LimitLevel(Filter):
    def __init__(self, type: UserType):
        self.type = type

    async def __call__(self, update: any, **data) -> bool:
        user: UserModel = data.get("user")
        if user:
            return user.type.value <= self.type.value
        return False
