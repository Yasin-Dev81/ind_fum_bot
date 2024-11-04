from db.base import get_session
from db.models import Plan


def read_alls() -> list[Plan]:
    with get_session() as session:
        return session.query(Plan.id, Plan.title).order_by(Plan.price).all()


def read(pk) -> Plan:
    with get_session() as session:
        return session.query(Plan).get(pk)
