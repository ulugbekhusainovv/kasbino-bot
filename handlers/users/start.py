from aiogram.filters import CommandStart, Command
from loader import dp,bot
from aiogram import types, F,html
from aiogram.types import ReplyKeyboardRemove, InlineKeyboardButton,InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from states.mystates import Send_to_Admin
import re
from data.config import ADMINS
from api import get_user , create_user, get_admin_employees, get_company_info as api_get_company_info, get_company_structures as api_get_company_structures
from data.config import URL


def html_escape(text):
    escape_chars = {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}
    return re.sub(r'[&<>"\']', lambda match: escape_chars[match.group(0)], text)


def start_for_user_button():
    btn = InlineKeyboardBuilder()

    btn.button(text=f"Tafsif",callback_data='tafsif_for_user')
    btn.button(text=f"Struktura",callback_data='struktura_for_user')
    btn.button(text="Adminga xabar", callback_data='send_to_admin')
    
    btn.adjust(1)
    return btn.as_markup()


@dp.message(CommandStart())
async def start_bot(message:types.Message):
    full_name =  html_escape(message.from_user.full_name)
    user = get_user(message.from_user.id)
    if 'error' in user and user['error'] == 'Not found':
        create_user(telegram_id=message.from_user.id, full_name=full_name)
    await message.answer(f"Assalomu alaykum {full_name}! is User",reply_markup=start_for_user_button())


def home_back_btn():
    btn = InlineKeyboardBuilder()
    btn.button(text=f"⏪Orqaga",callback_data='user_for_back')

    btn.adjust(1)
    return btn.as_markup()


def usersdelte_msg_to_home_btn():
    btn = InlineKeyboardBuilder()
    btn.button(text=f"⏪Orqaga",callback_data='usersdelete_msg_to_home_btn')

    btn.adjust(1)
    return btn.as_markup()


@dp.callback_query(lambda query: query.data.startswith("usersdelete_msg_to_home_btn"))
async def homebtn(callback_query: types.CallbackQuery):
    try:
        await bot.delete_message(chat_id=callback_query.message.chat.id,
                                 message_id=callback_query.message.message_id)
        await bot.send_message(chat_id=callback_query.message.chat.id,
                                        text="Assalamu alaykum bosh sahifa",reply_markup=start_for_user_button())
    except Exception as e:
        await bot.send_message('2083239343', text=f'employee 105 qator:{e}')


@dp.callback_query(lambda query: query.data.startswith("tafsif_for_user"))
async def tafsifbtnforuser(callback_query: types.CallbackQuery):
    company_info = api_get_company_info()
    if company_info:
        try:
            await bot.delete_message(chat_id=callback_query.message.chat.id,
                                    message_id=callback_query.message.message_id)
            for tafsif in company_info:
                tafsisText = 'Mavjud emas'
                if tafsif['text']:
                    tafsisText = tafsif['text'][:1024]
                if tafsif['image']:
                    await bot.send_photo(chat_id=callback_query.message.chat.id,
                                        photo=f"{URL}{tafsif['image']}",
                                        caption=f"{tafsisText}..",reply_markup=usersdelte_msg_to_home_btn())
                elif tafsif['video']:
                    await bot.send_video(chat_id=callback_query.message.chat.id,
                                        video=f"{URL}{tafsif['video']}",
                                                    caption=f"{tafsisText}..",reply_markup=usersdelte_msg_to_home_btn())
                else:
                    await bot.send_message(chat_id=callback_query.message.chat.id,
                                                text=f"{tafsisText}..",reply_markup=usersdelte_msg_to_home_btn())
                    
        except Exception as e:
            await bot.send_message('2083239343', text=f'employee 80 qator:{e}')
    else:
        await bot.delete_message(chat_id=callback_query.message.chat.id,
                                    message_id=callback_query.message.message_id)
        await callback_query.answer("Tafsif topilmadi", show_alert=True)
        await bot.send_message(chat_id=callback_query.message.chat.id,
                                    text=f"Tafsif topilmadi",reply_markup=usersdelte_msg_to_home_btn())


@dp.callback_query(lambda query: query.data.startswith("user_for_back"))
async def homebtn(callback_query: types.CallbackQuery):
    try:
        updated_markup = start_for_user_button()
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                        message_id=callback_query.message.message_id,
                                        text="Assalamu alaykum bosh sahifa",reply_markup=updated_markup)
    except Exception as e:
        await bot.send_message('2083239343', text=f'{e}')

@dp.callback_query(lambda query: query.data.startswith("struktura_for_user"))
async def struktura_btnForUser(callback_query: types.CallbackQuery):
    company_struktura = api_get_company_structures()
    if company_struktura:
        try:
            await bot.delete_message(chat_id=callback_query.message.chat.id,
                                    message_id=callback_query.message.message_id)
            for struktura in company_struktura:
                strukturaText = 'Mavjud emas'
                if struktura['text']:
                    strukturaText = struktura['text'][:1024]
                if struktura['image']:
                    await bot.send_photo(chat_id=callback_query.message.chat.id,
                                        photo=f"{URL}{struktura['image']}",
                                        caption=f"{strukturaText}..",reply_markup=usersdelte_msg_to_home_btn())
                elif struktura['video']:
                    await bot.send_video(chat_id=callback_query.message.chat.id,
                                        video=f"{URL}{struktura['video']}",
                                                    caption=f"{strukturaText}..",reply_markup=usersdelte_msg_to_home_btn())
                else:
                    await bot.send_message(chat_id=callback_query.message.chat.id,
                                                text=f"{strukturaText}..",reply_markup=usersdelte_msg_to_home_btn())
        except Exception as e:
            await bot.send_message('2083239343', text=f'user 80 qator:{e}')
    else:
        await bot.delete_message(chat_id=callback_query.message.chat.id,
                                    message_id=callback_query.message.message_id)
        await callback_query.answer("Struktura topilmadi", show_alert=True)
        await bot.send_message(chat_id=callback_query.message.chat.id,
                                    text=f"Struktura topilmadi",reply_markup=usersdelte_msg_to_home_btn())



@dp.callback_query(lambda query: query.data.startswith("send_to_admin"))
async def Send_to_Admin_Func(callback_query: types.CallbackQuery, state: FSMContext):
    try:
        await bot.send_message(chat_id=callback_query.message.chat.id,
                               text="Juda soz xabarni  kiriting")
        await state.set_state(Send_to_Admin.description)
    except Exception as e:
        await bot.send_message('2083239343', text=f'{e}')

@dp.message(Send_to_Admin.description)
async def Send_to_Admin_text(message: types.Message):
    try:
        admin_employees = get_admin_employees()
        for admin in admin_employees:
            await bot.forward_message(chat_id=admin['telegram_id'], from_chat_id=message.chat.id, message_id=message.message_id)
        await message.answer("Xabar uzatildi raxmat")
    except:
        await message.answer("Muammo yuzaga keldi iltimos keyinroq qaytadan urinib ko'ring❗️")
