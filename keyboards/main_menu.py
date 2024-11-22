from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_menu_keyboard(type_value: int) -> ReplyKeyboardMarkup:
    kb = [
        [
            KeyboardButton(text="پیام‌های خوانده نشده 📥"),
        ],
        [
            KeyboardButton(text="تمامی پیام‌ها ↙️"),
        ],
        [
            KeyboardButton(text="پیام‌های ارسال شده ↗️"),
        ],
        [
            KeyboardButton(text="یوزرها 👥"),
        ],
        [
            KeyboardButton(text="ارسال نوتیف 🔊"),
            KeyboardButton(text="سرچ 🔎"),
        ],
        [
            KeyboardButton(text="گزارش عملکرد 📈"),
        ],
        [
            KeyboardButton(text="اطلاعات من ℹ️"),
            KeyboardButton(text="قوانین 📝"),
        ],
    ]
    if type_value == 0:
        pass
    elif type_value == 1:
        kb.insert(
            1,
            [
                KeyboardButton(text="انجام نشده ❎"),
                KeyboardButton(text="در حال انجام 🔄"),
            ],
        )
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
                KeyboardButton(text="پیام‌های ارسال شده ↗️"),
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
