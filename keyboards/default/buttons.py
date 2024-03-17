from aiogram.utils.keyboard import ReplyKeyboardBuilder,KeyboardButton

def confirm_offer_btn():
    button = ReplyKeyboardBuilder()
    button.row(
        KeyboardButton(text="◀️ Orqaga"),
        KeyboardButton(text="Tasdiqlash ✅"),
    )
    button.adjust(2,2)
    return button.as_markup(resize_keyboard=True,one_time_keyboard=True,input_field_placeholder="Kiritilgan ma'lumotni tasdiqlang")


def complaint_btn():
    button = ReplyKeyboardBuilder()
    button.row(
        KeyboardButton(text='🔙 Orqaga'),
        KeyboardButton(text='Tasdiqlash ☑️'),
    )
    button.adjust(2,2)
    return button.as_markup(resize_keyboard=True,one_time_keyboard=True,input_field_placeholder="Kiritilgan ma'lumotni tasdiqlang")