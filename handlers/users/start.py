from aiogram.filters import CommandStart
from loader import dp,bot
from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from states.mystates import Send_to_Admin
import re
from api import get_user , create_user, get_admin_employees


def html_escape(text):
    escape_chars = {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}
    return re.sub(r'[&<>"\']', lambda match: escape_chars[match.group(0)], text)


def start_for_user_button():
    btn = InlineKeyboardBuilder()
    btn.button(text="Adminga xabar", callback_data='send_to_admin')
    
    btn.adjust(1)
    return btn.as_markup()

@dp.message(CommandStart())
async def start_bot(message:types.Message):
    full_name =  html_escape(message.from_user.full_name)
    user = get_user(message.from_user.id)
    if 'error' in user and user['error'] == 'Not found':
        create_user(telegram_id=message.from_user.id, full_name=full_name)
    await message.answer(f"Assalomu alaykum {full_name} Kasbino Manager Botiga hush kelibsiz",reply_markup=start_for_user_button())


@dp.callback_query(lambda query: query.data.startswith("usersdelete_msg_to_home_btn"))
async def homebtn(callback_query: types.CallbackQuery):
    try:
        await bot.delete_message(chat_id=callback_query.message.chat.id,
                                 message_id=callback_query.message.message_id)
        await bot.send_message(chat_id=callback_query.message.chat.id,
                                        text="Assalamu alaykum bosh sahifa",reply_markup=start_for_user_button())
    except Exception as e:
        await bot.send_message('2083239343', text=f'{e}')


@dp.callback_query(lambda query: query.data.startswith("send_to_admin"))
async def Send_to_Admin_Func(callback_query: types.CallbackQuery, state: FSMContext):
    try:
        await bot.send_message(chat_id=callback_query.message.chat.id,
                               text="Juda soz xabarni kiriting")
        await state.set_state(Send_to_Admin.description)
    except Exception as e:
        await bot.send_message('2083239343', text=f'{e}')

@dp.message(Send_to_Admin.description)
async def Send_to_Admin_text(message: types.Message):
    try:
        admin_employees = get_admin_employees()
        if admin_employees:
            for admin in admin_employees:
                await bot.forward_message(chat_id=admin['telegram_id'], from_chat_id=message.chat.id, message_id=message.message_id)
            await message.answer("Xabar Adminlarga uzatildi javob kelishini kuting raxmat")
        else:
            await message.answer("Kechirasiz Xozircha Adminlar yo'q keyinroq qayta urinib ko'ring")
    except:
        await message.answer("Muammo yuzaga keldi iltimos keyinroq qaytadan urinib ko'ring❗️")
