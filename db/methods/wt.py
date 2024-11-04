from db.base import get_session
from db.models import (
    User,
    WalletTransaction,
)


def create(user_id, method, amount, invoice, caption=None, status=False) -> int:
    with get_session() as session:
        wt = WalletTransaction(
            user_id=user_id,
            method=method,
            amount=amount,
            invoice=invoice,
            caption=caption,
            status=status,
        )
        session.add(wt)
        session.commit()
        return wt.id


def read(pk) -> WalletTransaction:
    with get_session() as session:
        return (
            session.query(
                WalletTransaction.id,
                WalletTransaction.amount,
                WalletTransaction.status,
                WalletTransaction.user_id,
                WalletTransaction.method,
                User.username.label("username"),
                User.referral_user_id.label("user_referral_user_id"),
            )
            .filter_by(id=pk)
            .join(User, User.id == WalletTransaction.user_id)
            .first()
        )


def update(pk, method=None, status=None, caption=None) -> bool:
    with get_session() as session:
        wt = session.query(WalletTransaction).get(pk)
        if method is not None:
            wt.method = method
        if status is not None:
            wt.status = status
        if caption is not None:
            wt.caption = caption
        session.commit()
        return True


def delete(pk) -> bool:
    with get_session() as session:
        wt = session.query(WalletTransaction).get(pk)
        if wt and not wt.status:
            session.delete(wt)
            session.commit()
            return True
        return False
