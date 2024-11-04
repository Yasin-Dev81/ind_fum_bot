import html
import asyncio
from sqlalchemy import String, cast, func
from sqlalchemy.orm import aliased

from utils.notif import send_admins_new_user
from db.base import get_session
from db.models import (
    User,
    UserType,
)


def create(tell_id: int, **kwargs) -> User:
    with get_session() as session:
        user = session.query(User).get(tell_id)
        if not user:
            user = User(
                id=tell_id,
                name=kwargs["name"],
                username=kwargs["username"],
                type=UserType.USER,
            )
            session.add(user)
            session.commit()
            asyncio.create_task(send_admins_new_user(user.id, admins()))
        return user


def read(pk) -> User:
    with get_session() as session:
        return session.query(User).get(pk)


def read_alls() -> list[User]:
    with get_session() as session:
        return session.query(User.id, User.name).all()


def admins() -> list[User]:
    with get_session() as session:
        return session.query(User).filter_by(type=UserType.ADMIN).all()


def is_admin(pk: int) -> bool:
    with get_session() as session:
        user = session.query(User).get(pk)
        if user and user.type == UserType.ADMIN:
            return True
        return False


def search(name: str) -> list[User]:
    with get_session() as session:
        return (
            session.query(User.id, User.name.label("title"))
            .filter(User.name.like("%" + name + "%"))
            .limit(10)
            .all()
        )
