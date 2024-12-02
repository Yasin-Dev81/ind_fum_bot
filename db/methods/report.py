from sqlalchemy import select, func, desc
import pandas as pd

from db.base import get_session
from db.models import (
    User,
    Message,
    Star,
    StatusType,
)


def user_count(by_type: bool = False):
    with get_session() as session:
        if by_type:
            result = session.execute(
                select(User.type, func.count(User.id)).group_by(User.type)
            ).all()
            df = pd.DataFrame(result, columns=["UserType", "UserCount"])
            user_df = df.pivot_table(
                index="UserType", values="UserCount", aggfunc="sum"
            )

            message_counts = session.execute(
                select(Message.sender_id, func.count(Message.id)).group_by(
                    Message.sender_id
                )
            ).all()
            message_df = pd.DataFrame(
                message_counts, columns=["SenderID", "MessageCount"]
            )
            return user_df.merge(
                message_df, left_on="UserType", right_on="SenderID", how="left"
            ).fillna(0)

        return session.scalar(select(func.count(User.id)))


def get_top_starred_messages():
    with get_session() as session:
        return session.execute(
            select(Message.id, Message.title, func.count(Star.star).label("star_count"))
            .join(Star, Star.message_id == Message.id)
            .where(Message.status == StatusType.PROCESS)
            .group_by(Message.id, Message.title)
            .order_by(desc("star_count"))
            .limit(3)
        ).all()
