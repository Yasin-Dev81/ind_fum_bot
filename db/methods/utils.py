import pandas as pd
from sqlalchemy import cast, String, and_, select, delete
from datetime import datetime, timedelta

from db.base import get_session
from db.models import (
    Config,
    WalletTransaction,
    ConfigTransaction,
    StatusMethod,
    WalletTransactionMethod,
)
from db.methods import ct as ct_db, wt as wt_db, user as user_db
from config import COINOS_GIFT, REFERALL_GIFT


async def add_gift_ct(pk) -> None:
    ct = ct_db.read(pk)
    wt_db.create(
        user_id=ct.user_id,
        method=WalletTransactionMethod.GIFT,
        amount=ct.amount * COINOS_GIFT,
        invoice="coinos-gift",
        status=True,
    )
    user_db.update_wallet(pk=ct.user_id, amount=ct.amount * COINOS_GIFT)


async def add_referall_gift_ct(pk) -> None:
    ct = ct_db.read(pk)
    if ct.user_referral_user_id:
        wt_db.create(
            user_id=ct.user_referral_user_id,
            method=WalletTransactionMethod.REFERAL,
            amount=ct.amount * REFERALL_GIFT,
            invoice="referall-gift",
            status=True,
        )
        user_db.update_wallet(
            pk=ct.user_referral_user_id, amount=ct.amount * REFERALL_GIFT
        )


async def add_gift_wt(pk) -> None:
    wt = wt_db.read(pk)
    wt_db.create(
        user_id=wt.user_id,
        method=WalletTransactionMethod.GIFT,
        amount=wt.amount * COINOS_GIFT,
        invoice="coinos-gift",
        status=True,
    )
    user_db.update_wallet(pk=wt.user_id, amount=wt.amount * COINOS_GIFT)


async def add_referall_gift_wt(pk) -> None:
    wt = wt_db.read(pk)
    if wt.user_referral_user_id:
        wt_db.create(
            user_id=wt.user_referral_user_id,
            method=WalletTransactionMethod.REFERAL,
            amount=wt.amount * REFERALL_GIFT,
            invoice="referall-gift",
            status=True,
        )
        user_db.update_wallet(
            pk=wt.user_referral_user_id, amount=wt.amount * REFERALL_GIFT
        )


def wallet_info(user_id) -> pd.DataFrame:
    with get_session() as session:
        wt = (
            session.query(
                cast(WalletTransaction.method, String), WalletTransaction.amount
            )
            .filter_by(user_id=user_id)
            .filter(WalletTransaction.status is True)
        )

        df = pd.read_sql(wt.statement, session.bind)

        return df.pivot_table(index="method", values="amount", aggfunc="sum")


def ct_info(user_id) -> pd.DataFrame:
    with get_session() as session:
        wt = (
            session.query(
                cast(ConfigTransaction.method, String), ConfigTransaction.amount
            )
            .filter_by(status=StatusMethod.PAIED)
            .outerjoin(Config, Config.id == ConfigTransaction.config_id)
            .filter(Config.user_id == user_id)
        )

        df = pd.read_sql(wt.statement, session.bind)

        return df.pivot_table(index="method", values="amount", aggfunc="sum")


def delete_trash_ct(days=1) -> None:
    with get_session() as session:
        delete_q = ConfigTransaction.__table__.delete().where(
            and_(
                ConfigTransaction.datetime_modified
                < datetime.now() - timedelta(days=days),
                ConfigTransaction.status != StatusMethod.PAIED,
            )
        )
        session.execute(delete_q)
        session.commit()


def delete_trash_c(days=1) -> None:
    with get_session() as session:
        one_day_ago = datetime.now() - timedelta(days=days)
        # subquery = select(ConfigTransaction.config_id).where(
        #     ConfigTransaction.config_id.isnot(None)
        # )
        session.execute(
            delete(Config)
            # .where(Config.id.not_in(subquery))
            .where(Config.datetime_modified < one_day_ago)
            .where(Config.status.is_(False))  # noqa: E712
            .where(Config.holdover.is_(False))  # noqa: E712
        )
        session.commit()
