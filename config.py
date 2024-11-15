from decouple import config
from dotenv import load_dotenv
import pytz

load_dotenv()


BOT_TOKEN = config("BOT_TOKEN")
PORT = config("PORT", default=8080, cast=int)
WEBHOOK_URL = config("WEBHOOK_URL")

SQLALCHEMY_DATABASE_URL = config("SQLALCHEMY_DATABASE_URL")

TIME_ZONE = pytz.timezone(config("TIME_ZONE", cast=str, default="Asia/Tehran"))
DATE_TIME_FMT = config("DATE_TIME_FMT", cast=str, default="%c")

PAGINATION = config("PAGINATION", default=5)

RULES_MSG = config("RULES_MSG", default="Rules")

USER_LEVEL = {
    0: config("DEVELOPER_NAME", default="توسعه دهنده"),
    1: config("ADMIN_NAME", default="ادمین (مدیر گروه)"),
    2: config("SUPERUSER_NAME", default="سوپر یوزر"),
    3: config("USER_NAME", default="یوزر پایه"),
}
