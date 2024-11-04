from db.base import get_session
from db.models import PremiumServer


def read_alls() -> list:
    with get_session() as session:
        return list(map(lambda i: i.name, session.query(PremiumServer.name).all()))
