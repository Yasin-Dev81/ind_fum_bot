from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_menu_keyboard(type_value: int) -> ReplyKeyboardMarkup:
    if type_value == 0:
        kb = [
            [
                KeyboardButton(text="پیام‌های خوانده نشده 📥"),
            ],
            [
                KeyboardButton(text="تمامی پیام‌ها ↙️"),
            ],
            [
                KeyboardButton(text="یوزرها"),
            ],
            [
                KeyboardButton(text="ارسال نوتیف"),
                KeyboardButton(text="سرچ"),
            ],
            [
                KeyboardButton(text="اطلاعات من ℹ️"),
                KeyboardButton(text="قوانین 📝"),
            ],
        ]
    elif type_value == 1:
        kb = [
            [
                KeyboardButton(text="پیام‌های خوانده نشده 📥"),
            ],
            [
                KeyboardButton(text="موضوعات انجام نشده ❎"),
            ],
            [
                KeyboardButton(text="تمامی پیام‌ها ↙️"),
            ],
            [
                KeyboardButton(text="ارسال نوتیف"),
                KeyboardButton(text="سرچ"),
            ],
            [
                KeyboardButton(text="اطلاعات من ℹ️"),
                KeyboardButton(text="قوانین 📝"),
            ],
        ]
    else:
        kb = [
            [
                KeyboardButton(text="ارتباط با مدیر گروه 🚀"),
            ],
            [
                KeyboardButton(text="پیام‌های خوانده نشده 📥"),
            ],
            [
                KeyboardButton(text="تمامی پیام‌ها ↙️"),
            ],
            [
                KeyboardButton(text="اطلاعات من ℹ️"),
                KeyboardButton(text="قوانین 📝"),
            ],
            [
                KeyboardButton(text="ارتباط با توسعه دهنده ⚠️"),
            ],
        ]

    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
