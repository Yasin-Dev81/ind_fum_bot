import asyncio

from utils import send_msg
from keyboards import get_notif_inline_keyboard
from config import PAGINATION
from db.base import get_session
from db.models import (
    User,
    UserType,
    Message,
    UserNotif,
    Star,
)


def create(title: str, text: str, for_admin: bool = True, **kwargs) -> User:
    with get_session() as session:
        receiver = None
        if for_admin:
            receiver = session.query(User).filter_by(type=UserType.ADMIN).first()
        else:
            receiver = session.query(User).filter_by(type=UserType.DEVELOPER).first()

        msg = Message(
            sender_id=kwargs["sender_id"],
            receiver_id=receiver.id,
            caption=text,
            title=title,
        )
        session.add(msg)

        # if kwargs.get("file_id"):
        #     pass

        session.commit()

        file_id = None
        user_notif = session.query(UserNotif).filter_by(user_id=receiver.id).first()
        if user_notif:
            file_id = user_notif.file_id

        asyncio.create_task(
            send_msg(
                user_id=receiver.id,
                text="پیام جدیدی دریافت شد.",
                markup=get_notif_inline_keyboard(msg.id),
                file_id=file_id,
            )
        )
        return msg


def reply(title: str | None, text: str, msg_id: int, **kwargs) -> User:
    with get_session() as session:
        r_msg = session.get(Message, msg_id)

        if not r_msg:
            raise ValueError(f"Message with id {msg_id} not found.")

        msg = Message(
            sender_id=kwargs["sender_id"],
            receiver_id=r_msg.sender_id,
            title=title,
            caption=text,
        )
        session.add(msg)

        # if kwargs.get("file_id"):
        #     pass

        session.commit()

        file_id = None
        user_notif = session.query(UserNotif).filter_by(user_id=r_msg.sender_id).first()
        if user_notif:
            file_id = user_notif.file_id
        asyncio.create_task(
            send_msg(
                user_id=r_msg.sender_id,
                text="پیام جدیدی دریافت شد.",
                markup=get_notif_inline_keyboard(msg.id),
                file_id=file_id,
            )
        )
        return msg


def uread_msgs(user_id: int, page: int = 1) -> list[Message]:
    with get_session() as session:
        # return session.query(Message).filter_by(receiver_id=user_id, seen=False).all()
        # offset_value = (page - 1) * PAGINATION
        return (
            session.query(Message)
            .join(User, User.id == Message.receiver_id)
            .outerjoin(Star, Star.message_id == Message.id)
            .filter(Message.receiver_id == user_id, Message.seen.is_(False))
            .order_by(User.type != UserType.SUPERUSER, Message.datetime_created)
            # .limit(PAGINATION)
            # .offset(offset_value)
            .all()
        )


def udone_msgs(user_id: int, page: int = 1) -> list[Message]:
    with get_session() as session:
        # return session.query(Message).filter_by(receiver_id=user_id, done=False).all()
        # offset_value = (page - 1) * PAGINATION
        return (
            session.query(Message)
            .join(User, User.id == Message.receiver_id)
            .outerjoin(Star, Star.message_id == Message.id)
            .filter(
                Message.receiver_id == user_id,
                Message.done.is_(False),
                Message.seen.is_(True),
            )
            .order_by(
                Star.star.desc(),
                User.type != UserType.SUPERUSER,
                Message.datetime_created,
            )
            # .limit(PAGINATION)
            # .offset(offset_value)
            .all()
        )


def all_msgs(user_id: int, page: int = 1) -> list[Message]:
    with get_session() as session:
        # return session.query(Message).filter_by(receiver_id=user_id).all()
        # offset_value = (page - 1) * PAGINATION
        return (
            session.query(Message)
            .join(User, User.id == Message.receiver_id)
            .outerjoin(Star, Star.message_id == Message.id)
            .filter(Message.receiver_id == user_id)
            .order_by(
                Star.star.desc(),
                User.type != UserType.SUPERUSER,
                Message.datetime_created,
            )
            # .limit(PAGINATION)
            # .offset(offset_value)
            .all()
        )


def msg(pk: int) -> Message:
    with get_session() as session:
        # return session.query(Message).get(pk)
        query = (
            session.query(
                Message.id,
                Message.tel_msg,
                Message.sender_id,
                Message.receiver_id,
                Message.done,
                Message.datetime_created,
                Message.datetime_modified,
                User.name.label("sender_name"),
                User.is_superuser,
                Star.star,
            )
            .join(User, User.id == Message.sender_id)
            .outerjoin(Star, Star.message_id == Message.id)
            .filter(Message.id == pk)
            .first()
        )
        return query


async def seen(pk: int) -> Message:
    def mark_seen():
        with get_session() as session:
            msg = session.get(Message, pk)
            if not msg:
                raise ValueError(f"Message with id {pk} not found.")

            msg.seen = True
            session.commit()
            return msg

    return await asyncio.to_thread(mark_seen)


async def done(pk: int) -> Message:
    def mark_done():
        with get_session() as session:
            msg = session.get(Message, pk)
            if not msg:
                raise ValueError(f"Message with id {pk} not found.")

            msg.done = True
            session.commit()
            return msg

    return await asyncio.to_thread(mark_done)


def user_media_notif(pk: int) -> UserNotif:
    with get_session() as session:
        return session.query(UserNotif).filter_by(user_id=pk).first()


def set_star(msg_id: int, count: int) -> str:
    with get_session() as session:
        r_msg = session.get(Message, msg_id)

        if not r_msg:
            raise ValueError(f"Message with id {msg_id} not found.")

        star = Star(
            message_id=msg_id,
            star=count,
        )
        session.add(star)
        session.commit()
        return count


def delete(pk: int) -> bool:
    with get_session() as session:
        ct = session.query(Message).get(pk)
        if ct:
            session.delete(ct)
            session.commit()
            return True
        return False
