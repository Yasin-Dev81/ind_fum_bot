from datetime import datetime

from db.base import get_session
from db.models import (
    User,
    Plan,
    Config,
)


def create(name, user, plan, status=False) -> int:
    with get_session() as session:
        config = Config(user_id=user.id, plan_id=plan.id, name=name, status=status)
        session.add(config)
        session.commit()
        return config.id


def read(pk) -> Config:
    with get_session() as session:
        return (
            session.query(
                Config.id,
                Config.name,
                Config.user_id,
                Plan.data_limit,
                Plan.expire_duration,
                User.type.label("user_type"),
                User.name.label("user_name"),
                Plan.price,
                Config.status,
                Config.holdover,
            )
            .filter(Config.id == pk)
            .join(Plan, Plan.id == Config.plan_id)
            .join(User, User.id == Config.user_id)
            .first()
        )


def update(pk, status=None, holdover=None) -> bool:
    with get_session() as session:
        config = session.query(Config).get(pk)

        config.status = status or config.status
        config.holdover = holdover or config.holdover
        session.commit()
        return True


def update_stats(pk, status=True, holdover=False) -> bool:
    with get_session() as session:
        config = session.query(Config).get(pk)

        config.status = status
        config.holdover = holdover
        session.commit()
        return True


def set_holdover(pk, status=False) -> None:
    with get_session() as session:
        config = session.query(Config).get(pk)
        config.holdover = status
        session.commit()


def timebased_create(
    start_date=datetime.now().replace(hour=0, minute=0, second=0, microsecond=0),
):
    with get_session() as session:
        return session.query(Config).filter(Config.datetime_created >= start_date).all()


def update_plan(pk: int, plan_id: int) -> bool:
    with get_session() as session:
        config = session.query(Config).get(pk)
        if config:
            config.plan_id = plan_id
            session.commit()
            return True
        return False
