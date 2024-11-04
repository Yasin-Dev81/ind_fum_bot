import asyncio

from utils.allerts import (
    amount_allert,
    user_expired_allert,
    user_limited_allert,
    reached_days_left_allert,
    reached_usage_percent_allert,
    user_updated_allert,
    user_deleted_allert,
)
from utils.notif import send_user_notif
from marz import (
    create_config as marz_create_config,
    config_info as marz_config_info,
    update_config as marz_update_config,
)
from db.methods import utils_db, ct_db, config_db, wt_db
from db.models import StatusMethod
from marz import update_config


async def payment_checker(pk, payment_amount, payment_received):
    if payment_amount <= payment_received:
        ct = ct_db.read(pk)
        if ct.holdover:
            config_info = await marz_config_info(f"{ct.config_name}-{ct.config_id}")
            if config_info.status == "active":
                config_db.update(ct.config_id, holdover=True)
            else:
                config_db.update(ct.config_id, status=True)
                asyncio.create_task(marz_update_config(ct.config_id, True))
        else:
            asyncio.create_task(marz_create_config(ct.config_id))
            config_db.update(ct.config_id, status=True)
        ct_db.update(pk, status=StatusMethod.PAIED)
        asyncio.create_task(utils_db.add_gift_ct(pk))
        asyncio.create_task(utils_db.add_referall_gift_ct(pk))
    else:
        asyncio.create_task(amount_allert(pk))


async def charge_payment_checker(pk, payment_amount, payment_received):
    wt = wt_db.read(pk)
    if payment_amount <= payment_received:
        wt_db.update(pk, status=True)

        asyncio.create_task(utils_db.add_gift_wt(pk))
        asyncio.create_task(utils_db.add_referall_gift_wt(pk))
    else:
        asyncio.create_task(
            send_user_notif(
                wt.user_id,
                "در شارژ کیف پول کمتر از مقداری که مشخص شده بود ارسال کردید لطفا به ادمین برای رفع مشکل پیام دهید!",
            )
        )


async def input_marz_datas_checker(datas):
    for data in datas:
        username = data.get("username")
        # admin = data.get("user").get("admin").get("username")
        if "-" in username:  # and admin == MARZ_USERNAME) or (admin is None):
            config_id = int(username.split("-")[-1])
            action = data.get("action")
            # enqueued_at = data.get("enqueued_at")
            # tries = data.get("tries")

            await marz_checker(config_id, action)


async def marz_checker(config_id, action):
    if action == "user_limited":
        asyncio.create_task(update_config(config_id))
        asyncio.create_task(user_limited_allert(config_id))
    elif action == "user_expired":
        asyncio.create_task(update_config(config_id))
        asyncio.create_task(user_expired_allert(config_id))
    elif action == "reached_usage_percent":
        asyncio.create_task(reached_usage_percent_allert(config_id))
    elif action == "reached_days_left":
        asyncio.create_task(reached_days_left_allert(config_id))
    elif action == "user_updated":
        asyncio.create_task(user_updated_allert(config_id))
    elif action == "user_deleted":
        config_db.update_stats(config_id, False)
        asyncio.create_task(user_deleted_allert(config_id))
    else:
        pass
