from datetime import datetime, timedelta

from db.base import get_session
from db.models import (
    ConfigTransaction,
    Discount,
)


def read(name) -> Discount:
    with get_session() as session:
        discount = session.query(Discount).filter_by(caption=name).first()
        if discount:
            r_count = (
                session.query(ConfigTransaction)
                .filter_by(discount_id=discount.id)
                .count()
            )
            if discount.is_active and r_count < discount.user_count:
                return discount
        raise ValueError("not activate discount!")


def read_with_id(pk) -> Discount:
    with get_session() as session:
        discount = session.query(Discount).get(pk)
        if discount:
            r_count = (
                session.query(ConfigTransaction)
                .filter_by(discount_id=discount.id)
                .count()
            )
            if discount.is_active and r_count < discount.user_count:
                return discount
        raise ValueError("not activate discount!")


def generate(duration: int, percentage: float, user_count: int = 1) -> str:
    with get_session() as session:
        now_date = datetime.now()
        end_date = now_date + timedelta(days=duration)
        dis = Discount(
            start_date=now_date,
            end_date=end_date,
            percentage=percentage,
            user_count=user_count,
        )
        session.add(dis)
        session.commit()
        return dis.caption


def generate_id(duration: int, percentage: float, user_count: int = 1) -> str:
    with get_session() as session:
        now_date = datetime.now()
        end_date = now_date + timedelta(days=duration)
        dis = Discount(
            start_date=now_date,
            end_date=end_date,
            percentage=percentage,
            user_count=user_count,
        )
        session.add(dis)
        session.commit()
        return dis.id
