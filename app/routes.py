from aiohttp.web_request import Request
from aiohttp import web

import asyncio

from config import COINOS_SECRET, MARZ_SECRET
from utils.allerts import not_confirmed_allert, not_confirmed_allert_wt
from .checker import input_marz_datas_checker, payment_checker, charge_payment_checker


async def check_crypto_payment(request: Request):
    try:
        pk = request.match_info.get("pk")
        data = await request.json()
        # print(pk, data)
        # xx = {
        #     "amount": 1805,
        #     "confirmed": True,
        #     "hash": "lnbc18050n1pnwr2tesp54zrmqc39ez049xd4rvuuprzjan4sd65gz6698a4wlns7tkxxp9pqpp58pr5cpjae2yvfavhff0ytvu9r84j3exka49ketrcdj240dqz083qhp5uwcvgs5clswpfxhm7nyfjmaeysn6us0yvjdexn9yjkv3k7zjhp2sxq9z0rgqcqpnrzjqt0uqszd8jthf96zsej4uhh4sktp06x60j3frkm2l3sz56msmv6nwrgpdvqqx5gqqyqqqqlgqqqp8zqqjq9qxpqysgq83549805rp6fah34z4h9usnlupfvhf8zel2mc2qpy0ywvssnk8vzjuh7h2d59h4j27mqt4mcenha09sah5483ekqefxwy002r8pd8sqp5e7mfm",
        #     "received": 1805,
        #     "text": "lnbc18050n1pnwr2tesp54zrmqc39ez049xd4rvuuprzjan4sd65gz6698a4wlns7tkxxp9pqpp58pr5cpjae2yvfavhff0ytvu9r84j3exka49ketrcdj240dqz083qhp5uwcvgs5clswpfxhm7nyfjmaeysn6us0yvjdexn9yjkv3k7zjhp2sxq9z0rgqcqpnrzjqt0uqszd8jthf96zsej4uhh4sktp06x60j3frkm2l3sz56msmv6nwrgpdvqqx5gqqyqqqqlgqqqp8zqqjq9qxpqysgq83549805rp6fah34z4h9usnlupfvhf8zel2mc2qpy0ywvssnk8vzjuh7h2d59h4j27mqt4mcenha09sah5483ekqefxwy002r8pd8sqp5e7mfm",
        #     "secret": "haji-haji",
        # }

        if data.get("secret") == COINOS_SECRET:
            payment_status = data.get("confirmed")
            payment_amount = data.get("amount")
            payment_received = data.get("received")

            if payment_status:
                asyncio.create_task(
                    payment_checker(pk, payment_amount, payment_received)
                )
            else:
                asyncio.create_task(not_confirmed_allert(pk))

            return web.Response(text="Payment processed successfully", status=200)
        else:
            return web.Response(text="Boro bache por-roo bro bache por-roo", status=400)

    except Exception as e:
        # Handle any exceptions that may occur
        print(f"Error processing payment: {str(e)}")
        return web.Response(text="Error processing payment", status=500)


async def check_crypto_charge_payment(request: Request):
    try:
        pk = request.match_info.get("pk")
        data = await request.json()
        # print(pk, data)
        # xx = {
        #     "amount": 1805,
        #     "confirmed": True,
        #     "hash": "lnbc18050n1pnwr2tesp54zrmqc39ez049xd4rvuuprzjan4sd65gz6698a4wlns7tkxxp9pqpp58pr5cpjae2yvfavhff0ytvu9r84j3exka49ketrcdj240dqz083qhp5uwcvgs5clswpfxhm7nyfjmaeysn6us0yvjdexn9yjkv3k7zjhp2sxq9z0rgqcqpnrzjqt0uqszd8jthf96zsej4uhh4sktp06x60j3frkm2l3sz56msmv6nwrgpdvqqx5gqqyqqqqlgqqqp8zqqjq9qxpqysgq83549805rp6fah34z4h9usnlupfvhf8zel2mc2qpy0ywvssnk8vzjuh7h2d59h4j27mqt4mcenha09sah5483ekqefxwy002r8pd8sqp5e7mfm",
        #     "received": 1805,
        #     "text": "lnbc18050n1pnwr2tesp54zrmqc39ez049xd4rvuuprzjan4sd65gz6698a4wlns7tkxxp9pqpp58pr5cpjae2yvfavhff0ytvu9r84j3exka49ketrcdj240dqz083qhp5uwcvgs5clswpfxhm7nyfjmaeysn6us0yvjdexn9yjkv3k7zjhp2sxq9z0rgqcqpnrzjqt0uqszd8jthf96zsej4uhh4sktp06x60j3frkm2l3sz56msmv6nwrgpdvqqx5gqqyqqqqlgqqqp8zqqjq9qxpqysgq83549805rp6fah34z4h9usnlupfvhf8zel2mc2qpy0ywvssnk8vzjuh7h2d59h4j27mqt4mcenha09sah5483ekqefxwy002r8pd8sqp5e7mfm",
        #     "secret": "haji-haji",
        # }

        if data.get("secret") == COINOS_SECRET:
            payment_status = data.get("confirmed")
            payment_amount = data.get("amount")
            payment_received = data.get("received")

            if payment_status:
                asyncio.create_task(
                    charge_payment_checker(pk, payment_amount, payment_received)
                )
            else:
                asyncio.create_task(not_confirmed_allert_wt(pk))

            return web.Response(text="Payment processed successfully", status=200)
        else:
            return web.Response(text="Boro bache por-roo bro bache por-roo", status=400)

    except Exception as e:
        # Handle any exceptions that may occur
        print(f"Error processing payment: {str(e)}")
        return web.Response(text="Error processing payment", status=500)


async def marzban_request(request: Request):
    try:
        secret = request.headers.get("x-webhook-secret")
        if secret == MARZ_SECRET:
            # data = [
            #     {
            #         "enqueued_at": 1726691787.559129,
            #         "send_at": 1726691787.559137,
            #         "tries": 0,
            #         "username": "JustYasin-3",
            #         "action": "reached_usage_percent",
            #         "user": {
            #             "proxies": {
            #                 "vless": {
            #                     "id": "2931e913-0f5c-4b78-9ee3-96ea1c014221",
            #                     "flow": "",
            #                 },
            #                 "trojan": {
            #                     "password": "61663nR1jUjEUAlCnZByFQ",
            #                     "flow": "",
            #                 },
            #             },
            #             "expire": 1727036999,
            #             "data_limit": 8053063680,
            #             "data_limit_reset_strategy": "no_reset",
            #             "inbounds": {
            #                 "vless": [
            #                     "ArvanCDN",
            #                     "VLESS_httpupgrade_HA",
            #                     "VLESS_TCP_HA",
            #                     "VLESS_H2_REALITY",
            #                     "GRPC_CF",
            #                 ],
            #                 "trojan": ["TROJAN_SERVERLESS"],
            #             },
            #             "note": None,
            #             "sub_updated_at": "2024-09-18T20:38:01",
            #             "sub_last_user_agent": "TelegramBot (like TwitterBot)",
            #             "online_at": "2024-09-18T20:38:31",
            #             "on_hold_expire_duration": None,
            #             "on_hold_timeout": None,
            #             "auto_delete_in_days": None,
            #             "username": "JustYasin-3",
            #             "status": "active",
            #             "used_traffic": 6986908728,
            #             "lifetime_used_traffic": 223263768876,
            #             "created_at": "2024-06-14T14:24:59",
            #             "links": [
            #                 "trojan://61663nR1jUjEUAlCnZByFQ@www.npmjs.com:80?security=none&type=ws&headerType=&path=%2Flovelive%3Fed%3D2560&host=worker-shy-thunder-1821-jafooaklf-adf-kossher-bashe-cheghad-gha.adfnho-adhfoiaj-aohoha-be-yad-yousef-khan-dadasham-basheh-jaans.workers.dev#%F0%9F%87%A9%F0%9F%87%AA%20NoneTls",
            #                 "trojan://61663nR1jUjEUAlCnZByFQ@digg.com:443?security=tls&type=ws&headerType=&path=%2Flovelive%3Fed%3D2560&host=hello-world-red-violet-f298ojfjww-rooberoo-com-to-my-hous-moder.golbahar-mikhan-metro-bezanan-ofioij-ohfjojofaaepq-jihiqhovzcoh.workers.dev&sni=hello-world-red-violet-f298ojfjww-rooberoo-com-to-my-hous-moder.golbahar-mikhan-metro-bezanan-ofioij-ohfjojofaaepq-jihiqhovzcoh.workers.dev&fp=firefox&alpn=http%2F1.1#%F0%9F%87%A9%F0%9F%87%AA%20digg",
            #                 "vless://2931e913-0f5c-4b78-9ee3-96ea1c014221@master.mongard.info:443?security=tls&type=httpupgrade&headerType=&path=%2Fray&host=master.mongard.info&sni=master.mongard.info&fp=chrome&alpn=http%2F1.1&allowInsecure=1#%F0%9F%87%A9%F0%9F%87%AA%20HZ",
            #                 "vless://2931e913-0f5c-4b78-9ee3-96ea1c014221@dash.admin.user.allah.mongard.games:443?security=tls&type=httpupgrade&headerType=&path=%2Fray&host=dash.admin.user.allah.mongard.games&sni=dash.admin.user.allah.mongard.games&fp=chrome&alpn=h2&allowInsecure=1#%F0%9F%87%A9%F0%9F%87%AA%20H2Z",
            #                 "vless://2931e913-0f5c-4b78-9ee3-96ea1c014221@37.152.181.120:80?security=none&type=tcp&headerType=&path=&host=#%F0%9F%87%A6%F0%9F%87%AA%20%5B2x%5D%20Special",
            #                 "vless://2931e913-0f5c-4b78-9ee3-96ea1c014221@137.184.246.119:443?security=reality&type=h2&headerType=&path=%2F&host=www.yahoo.com&sni=s.yimg.com&fp=chrome&pbk=-bxqyG-ihm1k_my5_fZP65QSKhHdXZk_Yo0Nljz3k28&sid=97eb75edd8230815#%F0%9F%87%BA%F0%9F%87%B8%20%5B0.5x%5D%20ymail",
            #                 "vless://2931e913-0f5c-4b78-9ee3-96ea1c014221@dash.mongard.info:443?security=tls&type=grpc&headerType=&serviceName=VRLdGZ9k&authority=&mode=gun&sni=mongard.info&fp=firefox&alpn=h2#%F0%9F%87%A9%F0%9F%87%AA%20CF%28grpc%29",
            #             ],
            #             "subscription_url": "https://popdev.me/sub/SnVzdFlhc2luLTMsMTcyNjY5MTkyMA_7PvbF5oS2",
            #             "excluded_inbounds": {"vless": [], "trojan": []},
            #             "admin": {
            #                 "username": "sing404_bot",
            #                 "is_sudo": False,
            #                 "telegram_id": None,
            #                 "discord_webhook": None,
            #             },
            #         },
            #         "used_percent": 86.76087766885757,
            #     }
            # ]
            datas = await request.json()

            asyncio.create_task(input_marz_datas_checker(datas))

            return web.Response(text="ok", status=200)
        else:
            return web.Response(text="Boro bache por-roo bro bache por-roo", status=400)
    except Exception as e:
        # Handle any exceptions that may occur
        print(f"Error processing payment: {str(e)}")
        return web.Response(text="Error processing payment", status=500)
