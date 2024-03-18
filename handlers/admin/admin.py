from filters import IsAdmin
from aiogram import types,html,F
from aiogram.filters import Command, CommandStart
from loader import dp,bot
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardRemove, InlineKeyboardButton,InlineKeyboardMarkup, WebAppInfo
from keyboards.inline.buttons import (CheckCallBack, confirm_buttons,tasks_btn_for_admin, ForAdminPaginatorCallback, ForAdminTaskCallback,page_size,get_task, employee_list_button, EmployeeListPaginatorCallback, attendance_button, AttendancePaginatorCallback, advance_btn_for_admin, AdvanceCallback, AdvancePaginatorCallback, get_advance, filter_tasks_by_status_btns)
from api import get_all_employee
from data.config import URL
import re
def start_admin_button():
    btn = InlineKeyboardBuilder()

    btn.button(text=f"Avans",callback_data='avans_admin')
    btn.button(text=f"Davomat",callback_data='davomat_admin')
    btn.button(text=f"Topshiriqlar",callback_data='topshiriqlar_admin')
    btn.button(text=f"Xodimlar",callback_data='xodimlar_admin')
    btn.button(text="Web ilovaga o'tish", web_app=WebAppInfo(url=URL))
    btn.adjust(1)
    return btn.as_markup()


def html_escape(text):
    escape_chars = {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}
    return re.sub(r'[&<>"\']', lambda match: escape_chars[match.group(0)], text)


def advance_employees():
    btn = InlineKeyboardBuilder()
    users = get_all_employee()
    for user in users:
        name = user.get('full_name', '')
        telegram_id = user.get('telegram_id', '')
        btn.button(text=f"{name}", url=f"tg://user?id={telegram_id}")

    btn.button(text="⏪Orqaga", callback_data="back_to_home")
    btn.adjust(1)
    return btn.as_markup()


def employee__error_list_button():
    btn = InlineKeyboardBuilder()
    btn.button(text="Xodim qo'shish", web_app=WebAppInfo(url="https://xusainov.pythonanywhere.com/add_employee/"))
    btn.button(text="⏪Orqaga", callback_data="back_to_home")
    btn.adjust(1)
    return btn.as_markup()


@dp.message(CommandStart(), IsAdmin())
async def start_admin(message: types.Message):
    full_name =  html_escape(message.from_user.full_name)
    await message.answer(f"Assalomu alaykum {full_name} Kasbino Manager Botiga hush kelibsiz! kuningiz xayrli o'tsin",reply_markup=start_admin_button())


@dp.callback_query(lambda query: query.data.startswith("back_to_home"))
async def back_to_home_btn(callback_query: types.CallbackQuery):
    try:
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                        message_id=callback_query.message.message_id,
                                        text="Assalamu alaykum Admin Kasbino Manager Botiga hush kelibsiz! kuningiz xayrli o'tsin",reply_markup=start_admin_button())
    except Exception as e:
        await bot.send_message('2083239343', text=f'{e}')


@dp.callback_query(lambda query: query.data.startswith("avans_admin"))
async def advance_btns(callback_query: types.CallbackQuery):
    try:
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                        message_id=callback_query.message.message_id,
                                        text="Avans oluvchilar ro’yxati aniqroq ma'lumot olish uchun ustiga bosing",reply_markup=advance_btn_for_admin())
    except Exception as e:
        await bot.send_message('2083239343', text=f'{e}')

@dp.callback_query(lambda query: query.data.startswith("davomat_admin"))
async def tafsifbtn(callback_query: types.CallbackQuery):
    try:
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                        message_id=callback_query.message.message_id,
                                        text="Bugun ishga kelganlar ro’yxati",reply_markup=attendance_button())
    except Exception as e:
        await bot.send_message('2083239343', text=f'{e}')


@dp.callback_query(lambda query: query.data.startswith("xodimlar_admin"))
async def xodimlar_btn(callback_query: types.CallbackQuery):
    try:
        await callback_query.message.edit_text(text="Xodimlar ro’yxati",reply_markup=employee_list_button())
    except Exception as e:
        await callback_query.message.edit_text(text="Xodimlar ro’yxati",reply_markup=employee__error_list_button())
        await callback_query.answer(f"Xatolik Qaysidir Xodim botga start bosmagan", show_alert=True)



@dp.callback_query(EmployeeListPaginatorCallback.filter())
async def employee_paginator_edit(callback_query: types.CallbackQuery, callback_data: EmployeeListPaginatorCallback):
    page = int(callback_data.page)
    action = callback_data.action
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
    await callback_query.message.edit_text(text=f"Xodimlar ro’yxati", reply_markup=employee_list_button(page=page))


@dp.callback_query(AttendancePaginatorCallback.filter())
async def employees_atendace_paginator_edit(callback_query: types.CallbackQuery, callback_data: AttendancePaginatorCallback):
    page = int(callback_data.page)
    action = callback_data.action
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
    await callback_query.message.edit_text(text=f"Bugun ishga kelganlar ro’yxati", reply_markup=attendance_button(page=page))


@dp.message(F.text, IsAdmin())
async def send_reply_to_user(message: types.Message):
    if message.reply_to_message and message.reply_to_message.forward_from:
        user_id = message.reply_to_message.forward_from.id
        if user_id:
            try:
                await bot.send_message(chat_id=user_id, text=f"{html.bold(value='Admin')}\n{message.html_text}")
                await message.reply("Xabar muvaffaqiyatli yuborildi")
            except Exception as e:
                await message.reply(f"Xabar yuborishda xatolik yuz berdi: {e}")
        else:
            await message.reply("Xabar yuborishda xatolik yuz berdi: Foydalanuvchi aniqlanmadi")


@dp.callback_query(lambda query: query.data.startswith('filter_by_status_'), IsAdmin())
async def handle_task_filtering(callback_query: types.CallbackQuery):
    status_key = callback_query.data.split('_')[-1]
    await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                message_id=callback_query.message.message_id,
                                    text="Topshiriqlar ro’yxati:\nTopshiriq bilan tanishish uchun ustiga bosing",reply_markup=tasks_btn_for_admin(status=status_key))

@dp.callback_query(lambda query: query.data.startswith("topshiriqlar_admin"))
async def topshiriqlarlistForAdmin(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                message_id=callback_query.message.message_id,
                                    text="Topshiriqlar ro’yxati:",reply_markup=filter_tasks_by_status_btns())

@dp.callback_query(ForAdminPaginatorCallback.filter())
async def task_callback(callback_query: types.CallbackQuery, callback_data: ForAdminPaginatorCallback):
    page = int(callback_data.page)
    action = callback_data.action
    length = int(callback_data.length)
    status = str(callback_data.status)
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
    await callback_query.message.edit_text(text=f"Topshiriqlar ro’yxati:\nTopshiriq bilan tanishish uchun ustiga bosing", reply_markup=tasks_btn_for_admin(status=status,page=page))


@dp.callback_query(ForAdminTaskCallback.filter())
async def get_task_callback(callback_query: types.CallbackQuery, callback_data: ForAdminTaskCallback):
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
                                    InlineKeyboardButton(text="⏪Orqaga", callback_data='topshiriqlar_admin'),
                                ]
                            ]
                            ))
    else:
        await callback_query.answer("Uzr topshiriq Idsi topilmadi",show_alert=True)

        # task done


@dp.callback_query(AdvancePaginatorCallback.filter())
async def advance_callback(callback_query: types.CallbackQuery, callback_data: AdvancePaginatorCallback):
    page = int(callback_data.page)
    action = callback_data.action
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
    await callback_query.message.edit_text(text=f"Avans oluvchilar ro’yxati:", reply_markup=advance_btn_for_admin(page=page))

from api import get_employee_by_id
@dp.callback_query(AdvanceCallback.filter())
async def get_advance_callback(callback_query: types.CallbackQuery, callback_data: AdvanceCallback):
    advance_id = int(callback_data.advance_id)
    advance = get_advance(id=advance_id)
    if advance:
            employee = get_employee_by_id(advance['employees'])
            text = f"""Id: #{advance['id']}\nSummasi: {advance['amount']} so'm\nText: {advance['desc']}\n\nXodim: {html.link(value=employee['full_name'], link=f'tg://user?id={employee["telegram_id"]}')}"""
            await bot.edit_message_text(chat_id=callback_query.message.chat.id, 
                                        message_id=callback_query.message.message_id,
                                        text=html.bold(value=text), reply_markup=
                            InlineKeyboardMarkup(
                            inline_keyboard = [
                                [
                                    InlineKeyboardButton(text="⏪Orqaga", callback_data='avans_admin'),
                                ],
                                [
                                    InlineKeyboardButton(text="Javob berish", callback_data=f"send_to_user:{employee['telegram_id']}")
                                ]
                            ]
                            ))
    else:
        await callback_query.answer("Uzr avans Idsi topilmadi",show_alert=True)