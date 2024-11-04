from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_menu_keyboard(is_used_gift: bool = True) -> ReplyKeyboardMarkup:
    kb = [
        [
            KeyboardButton(text="خرید کانفیگ 🛍"),
        ],
        [
            KeyboardButton(text="کانفیگ‌های من 🗂"),
            KeyboardButton(text="لینک رفرال 🔗"),
            # KeyboardButton(text="فاکتورهای من"),
        ],
        [
            KeyboardButton(text="شارژ کیف پول ⚡️"),
        ],
        [
            KeyboardButton(text="اطلاعات من ℹ️"),
            KeyboardButton(text="کیف پول 💵"),
        ],
        [
            KeyboardButton(text="قوانین 📝"),
        ],
    ]

    if not is_used_gift:
        kb.insert(
            0,
            [
                KeyboardButton(text="دریافت کانفیگ هدیه 🎁"),
            ],
        )

    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)


def get_main_menu_keyboard_admin() -> ReplyKeyboardMarkup:
    kb = [
        [
            KeyboardButton(text="خرید‌های امروز"),
        ],
        [
            KeyboardButton(text="ساخت کدتخفیف"),
        ],
        [
            KeyboardButton(text="یوزرها"),
            KeyboardButton(text="فاکتورها"),
        ],
        [KeyboardButton(text="نوتیف")],
        [KeyboardButton(text="سرچ")],
        [
            KeyboardButton(text="مدیا"),
        ],
    ]

    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
