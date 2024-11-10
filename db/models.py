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
    ADMIN = 0
    SUPERUSER = 1
    USER = 2


class MediaType(enum.Enum):
    PHOTO = "عکس"
    DOCUMENT = "فایل"
    VIDEO = "ویدئو"
    VOICE = "ویس"
    AUDIO = "فایل صوتی"
    VIDEO_NOTE = "ویدیو نوت (ویدیو مسیج)"


class Base(DeclarativeBase):
    type_annotation_map = {
        String128: types.String(length=128),
        String32: types.String(length=32),
        datetime: types.DateTime(timezone=True),
        UserType: Enum(UserType, default=UserType.USER),
        MediaType: Enum(MediaType),
        BigInteger: types.BigInteger(),
        CaptionText: types.Text(length=4096),
    }


class User(Base):
    __tablename__ = "user"
    __table_args__ = (PrimaryKeyConstraint("id", name="user_pk"),)

    id: Mapped[BigInteger]
    type: Mapped[UserType]
    first_name: Mapped[String128 | None]
    last_name: Mapped[String128 | None]
    username: Mapped[String32 | None]
    nick_name: Mapped[String128 | None]

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

    @property
    def name(self):
        if self.nick_name:
            return self.nick_name
        return " ".join([self.first_name or "", self.last_name or ""])


class UserNotif(Base):
    __tablename__ = "user_notif"
    __table_args__ = (
        PrimaryKeyConstraint("user_id", "file_id"),
        ForeignKeyConstraint(["user_id"], ["user.id"], ondelete="CASCADE"),
    )

    user_id: Mapped[BigInteger]
    file_id: Mapped[String128]


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

    seen: Mapped[bool] = mapped_column(default=False)

    caption: Mapped[CaptionText]

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


class MessageFile(Base):
    __tablename__ = "message_file"
    __table_args__ = (
        PrimaryKeyConstraint("message_id", "file_id", name="message_file_pk"),
        ForeignKeyConstraint(["message_id"], ["message.id"], ondelete="CASCADE"),
    )
    id: Mapped[int]

    message_id: Mapped[int]
    file_id: Mapped[String128 | None]
    media_type: Mapped[MediaType]


class Reply(Base):
    __tablename__ = "reply"
    __table_args__ = (
        PrimaryKeyConstraint("reply_in", "reply_to"),
        ForeignKeyConstraint(["reply_in"], ["message.id"], ondelete="CASCADE"),
        ForeignKeyConstraint(["reply_to"], ["message.id"], ondelete="CASCADE"),
    )

    reply_in: Mapped[int]
    reply_to: Mapped[int]

    def __repr__(self):
        return f"reply | {self.reply_in} : {self.reply_to}"

    def __str__(self):
        return f"reply | {self.reply_in} : {self.reply_to}"
