from filters import IsManager
from aiogram import types,html,F
from aiogram.filters import Command, CommandStart
from loader import dp,bot
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardRemove, InlineKeyboardButton,InlineKeyboardMarkup, WebAppInfo
from keyboards.inline.buttons import ( tasks_btn_for_manager, ForManagerPaginatorCallback, ForManagerTaskCallback,page_size,get_task, get_task_status, filter_tasks_by_status_btns, CheckCallBack, confirm_buttons,)
from aiogram.fsm.context import FSMContext
from states.mystates import Avans, Offer, Complaint
import re
from api import (post_advance as api_post_advance, get_all_employee as api_get_all_employ , get_admin_employees as api_get_admin_employees, post_offer as api_post_offer, post_complaint as api_post_complaint)
from data.config import URL
from datetime import datetime
def html_escape(text):
    escape_chars = {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}
    return re.sub(r'[&<>"\']', lambda match: escape_chars[match.group(0)], text)


def start_manager_button():
    btn = InlineKeyboardBuilder()

    btn.button(text=f"Topshiriqlar",callback_data='topshiriqlar_manager')
    btn.button(text="Avans", callback_data='manager_avans_callback')
    btn.button(text=f"Takliflar",callback_data='takliflar_forManager')
    btn.button(text=f"Shikoyatlar",callback_data='shikoyatlar_for_manager')
    btn.button(text="Topshiriq qo'shish", web_app=WebAppInfo(url=f"{URL}/simple_add_task/"))
    btn.adjust(1)
    return btn.as_markup()


@dp.message(CommandStart(), IsManager())
async def start_manager(message: types.Message):
    await message.answer("Salom manager", reply_markup=start_manager_button())

@dp.callback_query(lambda query: query.data.startswith("back_to_manager_home"))
async def manager_back_to_home_btn(callback_query: types.CallbackQuery):
    try:
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                        message_id=callback_query.message.message_id,
                                        text="Assalamu alaykum",reply_markup=start_manager_button())
    except Exception as e:
        await bot.send_message('2083239343', text=f'{e}')

@dp.callback_query(lambda query: query.data.startswith("topshiriqlar_manager"))
async def topshiriqlarlist(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                message_id=callback_query.message.message_id,
                                    text="Topshiriqlar ro’yxati:\nTopshiriq",reply_markup=filter_tasks_by_status_btns())


@dp.callback_query(lambda query: query.data.startswith('filter_by_status_'), IsManager())
async def handle_task_filtering(callback_query: types.CallbackQuery):
    status_key = callback_query.data.split('_')[-1]
    await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                message_id=callback_query.message.message_id,
                                    text="Topshiriqlar ro’yxati:\nTopshiriq bilan tanishish uchun ustiga bosing",reply_markup=tasks_btn_for_manager(status=status_key))
    
@dp.callback_query(ForManagerPaginatorCallback.filter())
async def task_callback(callback_query: types.CallbackQuery, callback_data: ForManagerPaginatorCallback):
    page = int(callback_data.page)
    action = callback_data.action
    status = callback_data.status
    length = int(callback_data.length)
    if action == 'next':
        if (page+1)*page_size >=length:
            page = page
        else:
            page += 1
    else:
        if page > 0:
            page = page - 1
        else:
            page=page
    await callback_query.message.edit_text(text=f"Topshiriqlar ro’yxati:\nTopshiriq bilan tanishish uchun ustiga bosing", reply_markup=tasks_btn_for_manager(status=status,page=page))


@dp.callback_query(ForManagerTaskCallback.filter())
async def get_task_callback(callback_query: types.CallbackQuery, callback_data: ForManagerTaskCallback):
    task_id = int(callback_data.task_id)
    task = get_task(id=task_id)
    if task:
            def get_status_display(status):
                status_map = {
                    'active': 'Aktiv',
                    'progress': 'Jarayonda',
                    'done': 'Bajarildi'
                }
                return status_map.get(status, status)
            
            employees = [employee['full_name'] for employee in task['employees']]
            accepted_employees = [employee['full_name'] for employee in task['accepted']]
            text = f"Id: #{task['id']}\nText: {task['name']}\nHolati: {get_status_display(task['task_status'])}\n\nXodimlar: {', '.join(employees)}"
            if accepted_employees:
                text += f"\n\nQabul qilganlar: {', '.join(accepted_employees)}"
            else:
                text += "\n\nQabul qilganlar: Mavjud emas"
            await bot.edit_message_text(chat_id=callback_query.message.chat.id, 
                                        message_id=callback_query.message.message_id,
                                        text=html.bold(value=text), reply_markup=
                            InlineKeyboardMarkup(
                            inline_keyboard = [
                                [
                                    InlineKeyboardButton(text="⏪Orqaga", callback_data='topshiriqlar_manager'),
                                ]
                            ]
                            ))
    else:
        await callback_query.answer("Uzr topshiriq Idsi topilmadi",show_alert=True)

        # task done



def manager_avans_btn():
    btn = InlineKeyboardBuilder()
    btn.button(text=f"Avans olish",callback_data='manager_avans')
    btn.button(text=f"⏪Orqaga",callback_data='back_to_manager_home')

    btn.adjust(1)
    return btn.as_markup()

@dp.callback_query(lambda query: query.data.startswith("manager_avans_callback"))
async def manager_avans_call(callback_query: types.CallbackQuery):
    try:
        await callback_query.message.edit_text(text="""Assalomu alaykum xodim. Avans har oyning 20-sanasida beriladi. Siz avans olish uchun arizani har oyning 17-sanasida soat 17:00 gacha ariza yuborishingiz mumkin. Avans uchun berilgan ariza dam olish kuni yoki bayram kuniga to'g'ri kelganda, keyingi 1-ish kunida ko'rib chiqiladi.""", reply_markup=manager_avans_btn())
    except Exception as e:
        await bot.send_message('2083239343', text=f'employee 506 qator:{e}')



@dp.callback_query(lambda query: query.data.startswith("manager_avans"))
async def manager_avans_olish_call(callback_query: types.CallbackQuery, state: FSMContext):
    try:
        await bot.send_message(chat_id=callback_query.message.chat.id, text="Juda soz avans miqdorini raqamlarda kiriting")
        await state.set_state(Avans.amount)
    except Exception as e:
        await bot.send_message('2083239343', text=f'employee 516 qator:{e} Avans dan xatolik')

@dp.message(F.text, Avans.amount)
async def manager_get_avans_amount(message: types.Message, state: FSMContext):
    if message.text.replace(" ", "").isdigit():
        amount = message.text
        await state.update_data({
            'amount': amount,
        })
        await message.answer("Juda soz endi Sababini kiriting")
        await state.set_state(Avans.desc)
    else:
        await message.reply("Iltimos faqat musbat raqam kiriting")
        await state.set_state(Avans.amount)
        

@dp.message(~F.text, Avans.desc)
async def manager_get_avans_not_text_info(message: types.Message, state: FSMContext):
    await message.answer("Iltimos faqat text kiriting")
    await state.set_state(Avans.desc)


@dp.message(F.text, Avans.desc)
async def manager_get_avans_info(message: types.Message, state: FSMContext):
    desc = message.text
    await state.update_data({
        'desc': desc,
        'telegram_id': message.from_user.id,
        'name': message.from_user.full_name
    })
    data = await state.get_data()
    text = f"""{html.bold(value="Tasdiqlang")}\nMiqdori: {data['amount']} so'm\nSababi: {data['desc']}"""
    await message.answer(text, reply_markup=confirm_buttons())
    await state.set_state(Avans.check)

@dp.callback_query(CheckCallBack.filter(), Avans.check, IsManager())
async def manager_send_info(callback_query: types.CallbackQuery, callback_data: CheckCallBack, state: FSMContext):
    check = callback_data.check
    await callback_query.answer(cache_time=60)
    if check:
        all_employees = api_get_all_employ()
        data = await state.get_data()
        name =  html_escape(data['name'])
        callback_query.message.from_user.id
        amount = int(''.join(str(data['amount']).split()))
        text = f"""{html.bold(value='Avans')}\n{html.bold(value='Ismi')}: {name}\n{html.bold(value='Miqdori')}: {amount} so'm\n{html.bold(value='Sababi')}: {data['desc']}"""
        try:
            admin_employees = api_get_admin_employees()
            for admin in admin_employees:
                await bot.send_message(chat_id=admin['telegram_id'], text=text, reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text="Profile", url=f"tg://user?id={data['telegram_id']}")
                    ],
                    [
                        InlineKeyboardButton(text="Javob berish", callback_data=f"send_to_user:{data['telegram_id']}")
                    ]
                ]))
            await callback_query.message.answer("""Sizning arizangiz qabul qilindi, arizangiz 1 ish kunida o'rganib chiqiladi.""",reply_markup=start_manager_button())
            for employee in all_employees:
                if str(employee['telegram_id']) == str(callback_query.from_user.id):
                    api_post_advance(desc=data['desc'], amount=amount, employee_id=employee['id'])
        except:
            await callback_query.message.answer(f"Muammo yuzaga keldi iltimos keyinroq qaytadan urinib ko'ringring❗️", reply_markup=start_manager_button())
    else:
        await callback_query.message.answer("Xabar Bekor qilindi",reply_markup=start_manager_button())
    await callback_query.message.delete()
    await state.clear()

def manager_taklif_btn():
    btn = InlineKeyboardBuilder()
    btn.button(text=f"Taklifni Kiritish",callback_data='enter_offerManager')
    btn.button(text=f"⏪Orqaga",callback_data='back_to_manager_home')

    btn.adjust(1)
    return btn.as_markup()

@dp.callback_query(lambda query: query.data.startswith("takliflar_forManager"))
async def taklifManager(callback_query: types.CallbackQuery):
    try:
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                        message_id=callback_query.message.message_id,
                                        text="Ushbu bo'limdan o'zingizni takliflaringizni qoldirishingiz mumkin.",reply_markup=manager_taklif_btn())
    except Exception as e:
        await bot.send_message('2083239343', text=f'employee 136 qator:{e}')



@dp.callback_query(lambda query: query.data.startswith("enter_offerManager"))
async def enter_offerManager_text(callback_query: types.CallbackQuery,state: FSMContext):
    try:
        try:
            await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
        except:
            pass
        await bot.send_message(chat_id=callback_query.message.chat.id,
                                        text='''Juda soz taklifni kiriting.''')
        await state.set_state(Offer.description)
    except Exception as e:
        await bot.send_message('2083239343', text=f':{e}')


@dp.message(~F.text, Offer.description)
async def manager_confirm_offer_not_text(message: types.Message, state: FSMContext):
    await message.answer("Iltimos faqat text kiriting")
    await state.set_state(Offer.description)


@dp.message(F.text, Offer.description)
async def manager_confirm_offer_text(message: types.Message, state: FSMContext):
    if isinstance(message.text, str):
        offer_text = message.text

        await state.update_data({
            "description": offer_text,
            'telegram_id': message.from_user.id,
            'name': message.from_user.full_name
        })
        await message.reply(text="Xabarni Tasdiqlysizmi? ⬇️", reply_markup=confirm_buttons())
        await state.set_state(Offer.check)


@dp.callback_query(CheckCallBack.filter(), Offer.check, IsManager())
async def manager_send_offer_to_admin(callback_query: types.CallbackQuery, callback_data: CheckCallBack, state: FSMContext):
    check = callback_data.check
    all_employees = api_get_all_employ()
    registration_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await callback_query.answer(cache_time=60)
    if check:
        data = await state.get_data()
        name =  html_escape(data['name'])
        text = f"""{html.bold(value='Taklif')}\n{html.bold(value='Ismi')}: {name}\n{html.bold(value='Text')}: {data['description']}"""
        try:
            admin_employees = api_get_admin_employees()
            for admin in admin_employees:
                await bot.send_message(chat_id=admin['telegram_id'], text=text, reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text="Profile", url=f"tg://user?id={data['telegram_id']}")
                    ],
                    [
                        InlineKeyboardButton(text="Javob berish", callback_data=f"send_to_user:{data['telegram_id']}")
                    ]]))
            await callback_query.message.answer("Taklifingizni qoldirganingiz uchun rahmat, taklifingiz ma'muriyat tomonidan o'rganib chiqiladi.",reply_markup=start_manager_button())
            for employee in all_employees:
                if str(employee['telegram_id']) == str(callback_query.from_user.id):
                    api_post_offer(desc=data['description'], add_date=registration_date, employee_id=employee['id'])
        except:
            await callback_query.message.answer("Muammo yuzaga keldi iltimos keyinroq qaytadan urinib ko'ring❗️",reply_markup=start_manager_button())
    else:
        await callback_query.message.answer("Xabar Bekor qilindi",reply_markup=start_manager_button())
    await callback_query.message.delete()
    await state.clear()


@dp.callback_query(lambda query: query.data.startswith("shikoyatlar_for_manager"))
async def manager_entered_complaint(callback_query: types.CallbackQuery):
    try:
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                        message_id=callback_query.message.message_id,
                                        text='''Ushbu bo'limdan o'zingizni shikoyatlaringizni qoldirishingiz mumkin.''',reply_markup=
                                        InlineKeyboardMarkup(
                            inline_keyboard = [
                                [
                                    InlineKeyboardButton(text="Shikoyatni Kiritish", callback_data='manager_enter_complaint'),
                                ],
                                [
                                    InlineKeyboardButton(text="⏪Orqaga", callback_data='home'),
                                ]
                            ]
    ))
    except Exception as e:
        await bot.send_message('2083239343', text=f'employee 267 qator:{e}')


@dp.callback_query(lambda query: query.data.startswith("manager_enter_complaint"))
async def manager_enter_complaint(callback_query: types.CallbackQuery, state: FSMContext):
    try:
        try:
            await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
        except:
            pass
        await bot.send_message(chat_id=callback_query.message.chat.id,
                               text='''Shikoyatni yozma ravishda kiriting.''')
        await state.set_state(Complaint.description)
    except Exception as e:
        await bot.send_message('2083239343', text=f':{e}')


@dp.message(~F.text, Complaint.description)
async def manager_confirm_complaint_not_text(message: types.Message, state: FSMContext):
    await message.answer("Iltimos faqat text kiriting")
    await state.set_state(Complaint.description)


@dp.message(F.text, Complaint.description)
async def manager_confirm_complaint_text(message: types.Message, state: FSMContext):
    if isinstance(message.text, str):
        complaint_text = message.text
        await state.update_data({
            "description": complaint_text,
            'telegram_id': message.from_user.id,
            'name': message.from_user.full_name
        })
        await message.reply(text="Shikoyatni Tasdiqlysizmi? ⬇️", reply_markup=confirm_buttons())
        await state.set_state(Complaint.check)

@dp.callback_query(CheckCallBack.filter(), Complaint.check, IsManager())
async def manager_send_complaint_text(callback_query: types.CallbackQuery, callback_data: CheckCallBack, state: FSMContext):
    check = callback_data.check
    all_employees = api_get_all_employ()
    registration_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await callback_query.answer(cache_time=60)
    if check:
        data = await state.get_data()
        name =  html_escape(data['name'])
        text = f"""{html.bold(value='Shikoyat')}\n{html.bold(value='Ismi')}: {name}\n{html.bold(value='Text')}: {data['description']}"""
        try:
            admin_employees = api_get_admin_employees()
            for admin in admin_employees:
                await bot.send_message(chat_id=admin['telegram_id'], text=text, reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text="Profile", url=f"tg://user?id={data['telegram_id']}")
                    ],
                    [
                        InlineKeyboardButton(text="Javob berish", callback_data=f"send_to_user:{data['telegram_id']}")
                    ]
                ]))
            await callback_query.message.answer("Shikoyatingizni qoldirganingiz uchun rahmat, shikoyatingiz ma'muriyat tomonidan o'rganib chiqiladi.",reply_markup=start_manager_button())
            for employee in all_employees:
                if str(employee['telegram_id']) == str(callback_query.from_user.id):
                    api_post_complaint(desc=data['description'], add_date=registration_date, employee_id=employee['id'])
        except:
            await callback_query.message.answer(f"Muammo yuzaga keldi iltimos keyinroq qaytadan urinib ko'ring❗️",reply_markup=start_manager_button())
    else:
        await callback_query.message.answer("Shikoyat Bekor qilindi Raxmat",reply_markup=start_manager_button())
    await callback_query.message.delete()
    await state.clear()

