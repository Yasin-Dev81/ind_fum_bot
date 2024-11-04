from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.schema import PrimaryKeyConstraint, ForeignKeyConstraint
from sqlalchemy.sql import func
from sqlalchemy import types, Enum
from typing import NewType
from datetime import datetime
import enum


String128 = NewType("String128", str)
String32 = NewType("String32", str)
String8 = NewType("String8", str)
BigInteger = NewType("BigInteger", int)
CaptionText = NewType("CaptionText", str)


class UserType(enum.Enum):
    ADMIN = "ادمین"
    USER = "یوزر"
    SUPERUSER = "سوپر یوزر"



class Base(DeclarativeBase):
    type_annotation_map = {
        String128: types.String(length=128),
        String32: types.String(length=32),
        datetime: types.DateTime(timezone=True),
        UserType: Enum(UserType, default=UserType.USER),
        BigInteger: types.BigInteger(),
        CaptionText: types.Text(length=4096),
    }


class User(Base):
    __tablename__ = "user"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="user_pk"),
    )

    id: Mapped[BigInteger]
    type: Mapped[UserType]
    name: Mapped[String128]
    username: Mapped[String32 | None]

    datetime_created: Mapped[datetime] = mapped_column(
        types.DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    datetime_modified: Mapped[datetime] = mapped_column(
        types.DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def __repr__(self):
        return f"user | {self.name} | {self.type.value}"

    def __str__(self):
        return f"user | {self.name} | {self.type.value}"



class Message(Base):
    __tablename__ = "message"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="message_pk"),
        ForeignKeyConstraint(["sender_id"], ["user.id"], ondelete="CASCADE"),
        ForeignKeyConstraint(["receiver_id"], ["user.id"], ondelete="CASCADE"),
    )

    id: Mapped[int]
    sender_id: Mapped[BigInteger]
    receiver_id: Mapped[BigInteger]
    answered: Mapped[bool] = mapped_column(default=False)

    caption: Mapped[CaptionText]
    file_id: Mapped[String128 | None]

    datetime_created: Mapped[datetime] = mapped_column(
        types.DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    datetime_modified: Mapped[datetime] = mapped_column(
        types.DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def __repr__(self):
        return f"msg | {self.sender_id} : {self.receiver_id}"

    def __str__(self):
        return f"msg | {self.sender_id} : {self.receiver_id}"
