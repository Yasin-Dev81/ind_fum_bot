import glv


async def block_user(user_id: int):
    try:
        await glv.bot.send_message(
            user_id, "شما به علت رعایت نکردن قوانین بات از طرف مدیر گروه بلاک شدید."
        )
        # await glv.bot.ban_chat_member(chat_id=user_id, user_id=user_id)
    except Exception:
        pass
