import asyncio

from utils.notif import send_msg
from keyboards import get_notif_user_inline_keyboard
from db.base import get_session
from db.models import (
    User,
    UserType,
    UserNotif,
)


def create(tell_id: int, **kwargs) -> User:
    with get_session() as session:
        user = session.query(User).get(tell_id)
        if not user:
            user = User(
                id=tell_id,
                first_name=kwargs["first_name"],
                last_name=kwargs["last_name"],
                username=kwargs["username"],
                type=UserType.USER,
            )
            session.add(user)
            session.commit()
            asyncio.create_task(
                send_msg(
                    admins().id, "new user", get_notif_user_inline_keyboard(user.id)
                )
            )
        return user


def read(pk) -> User:
    with get_session() as session:
        return session.query(User).get(pk)


def read_alls() -> list[User]:
    with get_session() as session:
        return session.query(User).all()


def admins() -> list[User]:
    with get_session() as session:
        return session.query(User).filter_by(type=UserType.ADMIN).first()


def set_superuser(pk: int) -> bool:
    with get_session() as session:
        user = session.query(User).get(pk)
        if not user:
            raise ValueError

        user.type = UserType.SUPERUSER
        session.commit()


def search(name: str) -> list[User]:
    with get_session() as session:
        return (
            session.query(User.id, User.name.label("title"))
            .filter(User.name.like("%" + name + "%"))
            .limit(10)
            .all()
        )


def set_notif_file_id(pk: int, file_id: str):
    with get_session() as session:
        user_notif = UserNotif(
            user_id=pk,
            file_id=file_id,
        )
        session.add(user_notif)
        session.commit()
