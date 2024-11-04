from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.schema import PrimaryKeyConstraint, ForeignKeyConstraint
from sqlalchemy.sql import func
from sqlalchemy import types, Enum
from typing import NewType
from datetime import datetime
from pytz import timezone
import enum
import random
import string

from config import TIME_ZONE


String128 = NewType("String128", str)
String32 = NewType("String32", str)
String8 = NewType("String8", str)
BigInteger = NewType("BigInteger", int)
CaptionText = NewType("CaptionText", str)


class UserType(enum.Enum):
    ADMIN = "ادمین"
    USER = "یوزر"
    SUPERUSER = "پریمیوم یوزر"
    CHANEL = "کانال تلگرام"


class TransactionMethod(enum.Enum):
    CARD = "کارت به کارت (برای کاربران پریمیوم)"
    LIGHTNING = "شبکه لایتنینگ بیت‌کوین"
    INTERNAL = "ولت"


class WalletTransactionMethod(enum.Enum):
    CARD = "کارت به کارت (برای کاربران پریمیوم)"
    LIGHTNING = "شبکه لایتنینگ بیت‌کوین"
    GIFT = "هدیه پرداخت با لایتنینگ"
    REFERAL = "شارژ رفرال"


class StatusMethod(enum.Enum):
    WAIT = 0
    INPAY = 1
    PAIED = 2


def generate_random_caption():
    return "".join(random.choices(string.ascii_letters, k=6))


class Base(DeclarativeBase):
    type_annotation_map = {
        String128: types.String(length=128),
        String32: types.String(length=32),
        String8: types.String(length=8),
        datetime: types.DateTime(timezone=True),
        UserType: Enum(UserType, default=UserType.USER),
        TransactionMethod: Enum(TransactionMethod),
        StatusMethod: Enum(StatusMethod),
        BigInteger: types.BigInteger(),
        CaptionText: types.Text(length=4096),
    }


class User(Base):
    __tablename__ = "user"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="user_pk"),
        ForeignKeyConstraint(["gift_plan"], ["plan.id"], ondelete="SET NULL"),
        ForeignKeyConstraint(["referral_user_id"], ["user.id"], ondelete="SET NULL"),
    )

    id: Mapped[BigInteger]
    type: Mapped[UserType]
    name: Mapped[String128]
    username: Mapped[String32]

    notif_enabled: Mapped[bool] = mapped_column(default=True)
    is_noob: Mapped[bool] = mapped_column(default=True)

    wallet: Mapped[BigInteger]

    referral_user_id: Mapped[BigInteger | None]
    gift_plan: Mapped[int | None] = mapped_column(default=1)
    is_used_gift: Mapped[bool] = mapped_column(default=False)

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


class Plan(Base):
    __tablename__ = "plan"
    __table_args__ = (PrimaryKeyConstraint("id", name="plan_pk"),)

    id: Mapped[int]
    title: Mapped[String128]
    caption: Mapped[CaptionText]

    data_limit: Mapped[int]
    expire_duration: Mapped[int]

    price: Mapped[int]

    def __repr__(self):
        return self.title


class Config(Base):
    __tablename__ = "config"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="config_pk"),
        ForeignKeyConstraint(["user_id"], ["user.id"], ondelete="CASCADE"),
        ForeignKeyConstraint(["plan_id"], ["plan.id"], ondelete="SET NULL"),
    )

    id: Mapped[int]
    user_id: Mapped[BigInteger]
    plan_id: Mapped[int | None]

    name: Mapped[String32]
    status: Mapped[bool] = mapped_column(default=False)
    holdover: Mapped[bool] = mapped_column(default=False)

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
        return f"{self.user_id} | {self.plan_id} | {self.status}"

    @property
    def marz_username(self):
        return "%s-%s" % (self.name, self.id)


class PremiumServer(Base):
    __tablename__ = "premium_server"
    __table_args__ = (PrimaryKeyConstraint("id", name="premium_server_pk"),)

    id: Mapped[int]
    name: Mapped[CaptionText]

    def __repr__(self):
        return self.name


class WalletTransaction(Base):
    __tablename__ = "wallet_transaction"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="wallet_transaction_pk"),
        ForeignKeyConstraint(["user_id"], ["user.id"], ondelete="SET NULL"),
    )

    id: Mapped[int]
    user_id: Mapped[BigInteger | None]
    caption: Mapped[CaptionText | None]

    status: Mapped[bool] = mapped_column(default=False)
    method: Mapped[WalletTransactionMethod]
    amount: Mapped[BigInteger]
    invoice: Mapped[CaptionText]

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
        return f"{self.id} | user-practice: {self.user_practice_id} | teacher: {self.teacher_id}"


class ConfigTransaction(Base):
    __tablename__ = "config_transaction"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="config_transaction_pk"),
        ForeignKeyConstraint(["config_id"], ["config.id"], ondelete="CASCADE"),
        ForeignKeyConstraint(["discount_id"], ["discount.id"], ondelete="SET NULL"),
    )

    id: Mapped[int]
    config_id: Mapped[int | None]
    caption: Mapped[CaptionText | None]

    discount_id: Mapped[int | None]
    status: Mapped[StatusMethod]
    holdover: Mapped[bool] = mapped_column(default=False)

    amount: Mapped[BigInteger]
    method: Mapped[TransactionMethod | None]
    invoice: Mapped[CaptionText | None]

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
        return f"{self.id}"


class Discount(Base):
    __tablename__ = "discount"
    __table_args__ = (PrimaryKeyConstraint("id", name="discount_pk"),)

    id: Mapped[int]
    caption: Mapped[String8] = mapped_column(
        default=generate_random_caption, unique=True
    )

    end_date: Mapped[datetime] = mapped_column(
        types.DateTime(timezone=True), nullable=False
    )
    start_date: Mapped[datetime] = mapped_column(
        types.DateTime(timezone=True), nullable=False
    )
    user_count: Mapped[int]

    percentage: Mapped[float]

    def __repr__(self) -> str:
        return self.caption

    @property
    def is_active(self):
        now = datetime.now(TIME_ZONE)
        return (
            self.start_date.replace(tzinfo=timezone("UTC"))
            <= now.replace(tzinfo=timezone("UTC"))
            <= self.end_date.replace(tzinfo=timezone("UTC"))
        )
