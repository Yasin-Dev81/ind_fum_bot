from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.schema import PrimaryKeyConstraint, ForeignKeyConstraint
from sqlalchemy.sql import func
from sqlalchemy import types, Enum, case, literal
from html import escape
from typing import NewType
from datetime import datetime
import enum


String128 = NewType("String128", str)
String60 = NewType("String60", str)
String32 = NewType("String32", str)
String8 = NewType("String8", str)
BigInteger = NewType("BigInteger", int)
CaptionText = NewType("CaptionText", str)


class UserType(enum.Enum):
    DEVELOPER = 0
    ADMIN = 1
    SUPERUSER = 2
    USER = 3
    BLOCKED = 4


class StatusType(enum.Enum):
    INQUEUE = 0
    PROCESS = 1
    DONE = 2
    DISABLE = 3


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
        String60: types.String(length=60),
        String32: types.String(length=32),
        datetime: types.DateTime(timezone=True),
        UserType: Enum(UserType, default=UserType.USER),
        StatusType: Enum(StatusType, default=StatusType.INQUEUE),
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

    @hybrid_property
    def name(self) -> str:
        if self.nick_name:
            return self.nick_name
        full_name = f"{self.first_name or ''} {self.last_name or ''}".strip()
        return full_name if full_name else (self.username or "Unknown")

    @name.expression
    def name(cls):
        return case(
            (cls.nick_name.is_not(None), cls.nick_name),  # noqa: E711
            else_=func.trim(
                func.concat(
                    func.coalesce(cls.first_name, ""),
                    " ",
                    func.coalesce(cls.last_name, ""),
                )
            ),
        )

    @hybrid_property
    def xname(self) -> str:
        if self.username:
            return f"@{self.username}"
        return "Unknown"

    @xname.expression
    def xname(cls):
        return func.coalesce(
            func.concat(literal("@"), cls.username), literal("Unknown")
        )

    @hybrid_property
    def is_superuser(self) -> str:
        return self.type == UserType.SUPERUSER


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
    # done: Mapped[bool] = mapped_column(default=False)
    status: Mapped[StatusType]

    title: Mapped[String60 | None]
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
        return f"{self.title} from {self.sender_id}"

    def __str__(self):
        return (
            f"<b>{self.title}</b>\n"
            f"<blockquote expandable>{self.caption}</blockquote>"
        )

    @hybrid_property
    def tel_msg(self) -> str:
        return (
            f"{escape(self.title or 'بدون عنوان')}\n"
            f"<blockquote expandable>{escape(self.caption)}</blockquote>"
        )

    @tel_msg.expression
    def tel_msg(cls):
        return func.concat(
            func.coalesce(cls.title, "بدون عنوان"),
            "\n<blockquote expandable>",
            cls.caption,
            "</blockquote>",
        )


class MessageFile(Base):
    __tablename__ = "message_file"
    __table_args__ = (
        PrimaryKeyConstraint("message_id", "file_id", name="message_file_pk"),
        ForeignKeyConstraint(["message_id"], ["message.id"], ondelete="CASCADE"),
    )
    id: Mapped[int]

    message_id: Mapped[int]
    file_id: Mapped[String128]
    media_type: Mapped[MediaType]


class Reply(Base):
    __tablename__ = "reply"
    __table_args__ = (
        PrimaryKeyConstraint("reply_in", "reply_to", name="reply_pk"),
        ForeignKeyConstraint(["reply_in"], ["message.id"], ondelete="CASCADE"),
        ForeignKeyConstraint(["reply_to"], ["message.id"], ondelete="CASCADE"),
    )

    reply_in: Mapped[int]
    reply_to: Mapped[int]

    def __repr__(self):
        return f"reply | {self.reply_in} : {self.reply_to}"

    def __str__(self):
        return f"reply | {self.reply_in} : {self.reply_to}"


class Star(Base):
    __tablename__ = "star"
    __table_args__ = (
        PrimaryKeyConstraint("message_id", "star", name="star_pk"),
        ForeignKeyConstraint(["message_id"], ["message.id"], ondelete="CASCADE"),
    )

    message_id: Mapped[int]
    star: Mapped[int]

    def __repr__(self):
        return f"reply | {self.reply_in} : {self.reply_to}"

    def __str__(self):
        return f"reply | {self.reply_in} : {self.reply_to}"
