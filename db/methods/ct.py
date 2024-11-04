from sqlalchemy import cast, String, desc

from db.base import get_session
from db.models import (
    User,
    Plan,
    Config,
    ConfigTransaction,
    Discount,
    StatusMethod,
)


def create(
    amount, config_id, status, method=None, invoice=None, caption=None, holdover=False, discount_id=None
) -> int:
    with get_session() as session:
        ct = ConfigTransaction(
            amount=amount,
            config_id=config_id,
            status=status,
            method=method,
            invoice=invoice,
            caption=caption,
            holdover=holdover,
            discount_id=discount_id
        )

        session.add(ct)
        session.commit()
        return ct.id


def read(pk) -> ConfigTransaction:
    with get_session() as session:
        return (
            session.query(
                ConfigTransaction.id,
                ConfigTransaction.amount,
                ConfigTransaction.status,
                ConfigTransaction.caption,
                ConfigTransaction.holdover,
                User.id.label("user_id"),
                User.username.label("username"),
                User.referral_user_id.label("user_referral_user_id"),
                Plan.title.label("plan_title"),
                Plan.price.label("plan_price"),
                Discount.caption.label("discount_caption"),
                Discount.percentage.label("discount_percentage"),
                Config.name.label("config_name"),
                Config.id.label("config_id"),
            )
            .filter_by(id=pk)
            .join(Config, Config.id == ConfigTransaction.config_id)
            .join(Plan, Plan.id == Config.plan_id)
            .join(User, User.id == Config.user_id)
            .outerjoin(Discount, Discount.id == ConfigTransaction.discount_id)
            .first()
        )


def update(pk, status, method=None, invoice=None, caption=None) -> ConfigTransaction:
    with get_session() as session:
        ct = session.query(ConfigTransaction).get(pk)
        if ct:
            ct.status = status
            if status == StatusMethod.PAIED:
                config = session.query(Config).get(ct.config_id)
                config.status = True
            if method:
                ct.method = method
            if invoice:
                ct.invoice = invoice
            if caption:
                ct.caption = caption
            session.commit()
            return ct


def delete(pk) -> bool:
    with get_session() as session:
        ct = session.query(ConfigTransaction).get(pk)
        if ct and not ct.status == StatusMethod.PAIED:
            session.delete(ct)
            session.commit()
            return True
        return False


def set_discount(discount, pk) -> ConfigTransaction:
    with get_session() as session:
        ct = session.query(ConfigTransaction).get(pk)
        ct.discount_id = discount.id
        ct.amount = ct.amount * (1 - discount.percentage)
        session.commit()
        return ct


def statusbased_ct(status=StatusMethod.INPAY):
    with get_session() as session:
        return (
            session.query(
                ConfigTransaction.id,
                (Config.name + " | " + cast(ConfigTransaction.id, String)).label(
                    "title"
                ),
            )
            .join(Config, Config.id == ConfigTransaction.config_id)
            .filter(ConfigTransaction.status == status)
            .all()
        )


def read_alls_with_config(config_pk):
    with get_session() as session:
        return (
            session.query(
                ConfigTransaction.id,
                (
                    ConfigTransaction.status
                    + " | "
                    + cast(ConfigTransaction.datetime_modified, String)
                ).label("title"),
            )
            .filter_by(config_id=config_pk)
            .order_by(desc(ConfigTransaction.datetime_modified))
            .all()
        )
