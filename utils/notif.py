import glv


async def send_msg(user_id: int, text: str, markup, file_id=None):
    try:
        if file_id:
            await glv.bot.send_voice(
                chat_id=user_id,
                voice=file_id,
                caption=text,
                reply_markup=markup,
            )
        else:
            await glv.bot.send_message(
                chat_id=user_id,
                text=text,
                reply_markup=markup,
            )
    except Exception:
        pass


async def send_msg_list(user_list, text, sender_id=None):
    for user in user_list:
        try:
            await glv.bot.send_message(user.id, text)
        except Exception:
            pass
    else:
        if sender_id is not None:
            try:
                await glv.bot.send_message(
                    sender_id, "پیام به همه کاربران با موفقیت ارسال شد."
                )
            except Exception:
                pass
