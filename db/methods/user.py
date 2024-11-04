import html
import asyncio
from sqlalchemy import String, cast, func
from sqlalchemy.orm import aliased

from utils.notif import send_user_notif, send_admins_new_user
from db.base import get_session
from db.models import (
    User,
    UserType,
    Config,
    ConfigTransaction,
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
                wallet=0,
            )
            session.add(user)
            session.commit()
            asyncio.create_task(send_admins_new_user(user.id, admins()))
        return user


def read(pk) -> User:
    with get_session() as session:
        referral_user = aliased(User)
        user = (
            session.query(
                User.id,
                User.name,
                User.username,
                User.type,
                User.is_used_gift,
                User.is_noob,
                User.wallet,
                User.gift_plan,
                referral_user.name.label("referral_name"),
                referral_user.username.label("referral_username"),
            )
            .outerjoin(referral_user, referral_user.id == User.referral_user_id)
            .filter(User.id == pk)
            .first()
        )
        # return session.query(User).get(pk)
        return user


def read_alls() -> list[User]:
    with get_session() as session:
        return session.query(User.id, User.name.label("title")).all()


def update(pk, referral_user_id, type=None, gift_plan_id=None) -> bool:
    with get_session() as session:
        user = session.query(User).get(pk)
        user.referral_user_id = referral_user_id
        if type:
            user.type = type
        if gift_plan_id:
            user.gift_plan = gift_plan_id
        session.commit()
        asyncio.create_task(
            send_user_notif(
                referral_user_id,
                f"کاربر {html.escape(user.name)} با لینک رفرال شما عضو بات شد.",
            )
        )
        return True


def update_wallet(pk, amount) -> bool:
    with get_session() as session:
        user = session.query(User).get(pk)
        if user:
            user.wallet = user.wallet + amount
            session.commit()
            asyncio.create_task(
                send_user_notif(
                    pk,
                    f"{amount:,.0f} تومن از کیف پول شما کسر شد."
                    if amount <= 0
                    else f"{amount:,.0f} تومن به کیف پول شما اضافه شد.",
                )
            )
            return True


def update_notif_status(pk: int, status: bool) -> bool:
    with get_session() as session:
        user = session.query(User).get(pk)
        if user:
            user.notif_enabled = status
            session.commit()
            return True


def set_superuser(pk: int) -> User:
    with get_session() as session:
        user = session.query(User).get(pk)
        if user:
            if user.type == UserType.SUPERUSER:
                user.type = UserType.USER
                msg = "پریمیوم شما لغو شد!"
            else:
                user.type = UserType.SUPERUSER
                msg = "پریمیوم برای شما فعال شد!"
            session.commit()
            asyncio.create_task(
                send_user_notif(
                    pk,
                    msg,
                )
            )
            return user


def factors(user_id) -> list[ConfigTransaction]:
    with get_session() as session:
        return (
            session.query(
                ConfigTransaction.id,
                (Config.name + " | " + cast(ConfigTransaction.id, String)).label(
                    "title"
                ),
            )
            .join(Config, Config.id == ConfigTransaction.config_id)
            .filter(Config.user_id == user_id)
            .all()
        )


def admins() -> list[User]:
    with get_session() as session:
        return session.query(User).filter_by(type=UserType.ADMIN).all()


def configs(user_id) -> list[Config]:
    with get_session() as session:
        return (
            session.query(Config.id, Config.name.label("title"))
            .filter_by(user_id=user_id)
            .all()
        )


def referall_count(user_id):
    with get_session() as session:
        return (
            session.query(func.count(User.id)).filter_by(referral_user_id=user_id).all()
        )


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


def read_alls_with_notif() -> list[User]:
    with get_session() as session:
        return session.query(User).filter_by(notif_enabled=True).all()


def del_noob(pk: int) -> bool:
    with get_session() as session:
        user = session.query(User).get(pk)
        if user:
            user.is_noob = False
            session.commit()
            return True
        return False


def used_gift(pk: int) -> bool:
    with get_session() as session:
        user = session.query(User).get(pk)
        if user:
            user.is_used_gift = True
            session.commit()
            return True
        return False
