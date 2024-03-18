from aiogram.filters import CommandStart, Command
from loader import dp,bot
from aiogram import types, F,html
from aiogram.types import ReplyKeyboardRemove, InlineKeyboardButton,InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from states.mystates import Avans, Offer, Complaint,Send_to_user, Send_Info_to_Admin, Work_start_to_Admin, Work_finish_to_Admin
from keyboards.default.buttons import confirm_offer_btn,complaint_btn
from keyboards.inline.buttons import TaskCallback
import asyncio,re
from keyboards.inline.buttons import (CheckCallBack, confirm_buttons,task_btn, PaginatorCallback, TaskCallback,page_size,get_task)
from filters import IsEmployee, IsAdmin
from api import (get_task as api_get_task, update_task_status as api_update_task_status, update_task_accepted as api_update_task_accepted, get_all_employee as api_get_all_employ, post_advance as api_post_advance, post_offer as api_post_offer,post_complaint as api_post_complaint, set_employee_status as api_set_employee_status, get_employee as api_get_employ, get_company_info as api_get_company_info, get_company_structures as api_get_company_structures, post_attendance as api_post_attendance, get_admin_employees as api_get_admin_employees, get_manager_employees as api_get_manager_employees, get_all_category_info, get_all_category_structure)
from datetime import datetime
from data.config import URL

def html_escape(text):
    escape_chars = {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}
    return re.sub(r'[&<>"\']', lambda match: escape_chars[match.group(0)], text)


def start_button():
    btn = InlineKeyboardBuilder()

    btn.button(text=f"Tafsif",callback_data='tafsif_list_for_employee')
    btn.button(text=f"Struktura",callback_data='struktura_list_for_employee')
    btn.button(text=f"Takliflar",callback_data='takliflar_for_employee')
    btn.button(text=f"Shikoyatlar",callback_data='shikoyatlar_for_employee')
    btn.button(text=f"Davomat",callback_data='davomat_for_employee')    
    btn.button(text=f"Avans",callback_data='avans_callback_for_employee')
    btn.button(text=f"Topshiriqlar",callback_data='topshiriqlar_list_for_employee')
    btn.adjust(1,2,1,2,1)
    return btn.as_markup()


@dp.message(CommandStart(), IsEmployee())
async def start_bot(message:types.Message):
    full_name =  html_escape(message.from_user.full_name)
    await message.answer(f"Assalomu alaykum {full_name} Kasbino Manager Botiga hush kelibsiz!",reply_markup=start_button())

def home_back_btn():
    btn = InlineKeyboardBuilder()
    btn.button(text=f"⏪Orqaga",callback_data='home')

    btn.adjust(1)
    return btn.as_markup()


def delte_msg_to_home_btn():
    btn = InlineKeyboardBuilder()
    btn.button(text=f"⏪Orqaga",callback_data='delete_msg_to_home_btn')

    btn.adjust(1)
    return btn.as_markup()

def tafsif_category_btn():
    btn = InlineKeyboardBuilder()
    all_category_info = get_all_category_info()
    for category in all_category_info:
        btn.button(text=f"{category['name']}",callback_data=f"tafsif_for_employee_{category['id']}")
    btn.button(text=f"⏪Orqaga",callback_data='home')

    btn.adjust(1)
    return btn.as_markup()

@dp.callback_query(lambda query: query.data.startswith("tafsif_list_for_employee"))
async def tafsifbtn(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, 
                                message_id=callback_query.message.message_id,
                                text="Tafsifni ko'rish uchun kategoriyasini ustiga bosing", reply_markup=tafsif_category_btn())

@dp.callback_query(lambda query: query.data.startswith("tafsif_for_employee_"))
async def tafsifbtn(callback_query: types.CallbackQuery):
    category_id = int(callback_query.data.split('_')[-1])
    company_info = api_get_company_info()
    if company_info:
        try:
            await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
            for info in company_info:
                if info['category']['id'] == category_id:
                    tafsir_text = info['text'][:1024] if info['text'] else "Mavjud emas"
                    if info['pdf']:
                        await bot.send_document(chat_id=callback_query.message.chat.id, document=f"{URL}{info['pdf']}", caption=tafsir_text, reply_markup=delte_msg_to_home_btn())
                    elif info['image']:
                        await bot.send_photo(chat_id=callback_query.message.chat.id, photo=f"{URL}{info['image']}", caption=tafsir_text, reply_markup=delte_msg_to_home_btn())
                    elif info['video']:
                        await bot.send_video(chat_id=callback_query.message.chat.id, video=f"{URL}{info['video']}", caption=tafsir_text, reply_markup=delte_msg_to_home_btn())
                    else:
                        await bot.send_message(chat_id=callback_query.message.chat.id, text=tafsir_text, reply_markup=delte_msg_to_home_btn())
        except Exception as e:
            await bot.send_message(chat_id=callback_query.message.chat.id, text="Xatolik yuz berdi iltimos keyinroq qayta urinib ko'ring")
            await bot.send_message('2083239343', text=f'employee 80 qator:{e}')
    else:
        await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
        await callback_query.answer("Tafsif topilmadi", show_alert=True)
        await bot.send_message(chat_id=callback_query.message.chat.id, text=f"Tafsif topilmadi", reply_markup=delte_msg_to_home_btn())

@dp.callback_query(lambda query: query.data.startswith("home"))
async def homebtn(callback_query: types.CallbackQuery):
    try:
        updated_markup = start_button()
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                        message_id=callback_query.message.message_id,
                                        text="Assalamu alaykum Kasbino Manager Botiga hush kelibsiz!",reply_markup=updated_markup)
    except Exception as e:
        await bot.send_message('2083239343', text=f'employee 94 qator:{e}')


@dp.callback_query(lambda query: query.data.startswith("delete_msg_to_home_btn"))
async def homebtn(callback_query: types.CallbackQuery):
    try:
        await bot.delete_message(chat_id=callback_query.message.chat.id,
                                 message_id=callback_query.message.message_id)
        await bot.send_message(chat_id=callback_query.message.chat.id,
                                        text="Assalamu alaykum bosh sahifa",reply_markup=start_button())
    except Exception as e:
        await bot.send_message('2083239343', text=f'employee 105 qator:{e}')
        


def struktura_category_btn():
    btn = InlineKeyboardBuilder()
    all_category_structure = get_all_category_structure()
    for category in all_category_structure:
        btn.button(text=f"{category['name']}",callback_data=f"struktura_for_employee_{category['id']}")
    btn.button(text=f"⏪Orqaga",callback_data='home')

    btn.adjust(1)
    return btn.as_markup()


@dp.callback_query(lambda query: query.data.startswith("struktura_list_for_employee"))
async def struktura_category(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, 
                                message_id=callback_query.message.message_id,
                                text="Strukturani ko'rish uchun kategoriyasini ustiga bosing", reply_markup=struktura_category_btn())

@dp.callback_query(lambda query: query.data.startswith("struktura_for_employee_"))
async def tafsifbtn(callback_query: types.CallbackQuery):
    category_id = int(callback_query.data.split('_')[-1])
    company_structure = api_get_company_structures()
    if company_structure:
        try:
            await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
            for struktura in company_structure:
                if struktura['category']['id'] == category_id:
                    struktura_text = struktura['text'][:1024] if struktura['text'] else "Mavjud emas"
                    if struktura['pdf']:
                        await bot.send_document(chat_id=callback_query.message.chat.id, document=f"{URL}{struktura['pdf']}", caption=struktura_text, reply_markup=delte_msg_to_home_btn())
                    elif struktura['image']:
                        await bot.send_photo(chat_id=callback_query.message.chat.id, photo=f"{URL}{struktura['image']}", caption=struktura_text, reply_markup=delte_msg_to_home_btn())
                    elif struktura['video']:
                        await bot.send_video(chat_id=callback_query.message.chat.id, video=f"{URL}{struktura['video']}", caption=struktura_text, reply_markup=delte_msg_to_home_btn())
                    else:
                        await bot.send_message(chat_id=callback_query.message.chat.id, text=struktura_text, reply_markup=delte_msg_to_home_btn())
        except Exception as e:
            await bot.send_message(chat_id=callback_query.message.chat.id, text="Xatolik yuz berdi iltimos keyinroq qayta urinib ko'ring")
            await bot.send_message('2083239343', text=f':{e}')
    else:
        await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
        await callback_query.answer("Struktura topilmadi", show_alert=True)
        await bot.send_message(chat_id=callback_query.message.chat.id, text=f"Struktura topilmadi", reply_markup=delte_msg_to_home_btn())

def menu():
    btn = InlineKeyboardBuilder()
    btn.button(text=f"Taklifni Kiritish",callback_data='enter_offer')
    btn.button(text=f"⏪Orqaga",callback_data='home')

    btn.adjust(1)
    return btn.as_markup()

@dp.callback_query(lambda query: query.data.startswith("takliflar_for_employee"))
async def takliflar_btn(callback_query: types.CallbackQuery):
    try:
        updated_markup = menu()
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                        message_id=callback_query.message.message_id,
                                        text="Ushbu bo'limdan o'zingizni takliflaringizni qoldirishingiz mumkin.",reply_markup=updated_markup)
    except Exception as e:
        await bot.send_message('2083239343', text=f'employee 136 qator:{e}')


@dp.callback_query(lambda query: query.data.startswith("send_to_user:"))
async def send_to_user(callback_query: types.CallbackQuery, state: FSMContext):
    _, user_id = callback_query.data.split(":")
    user_id = int(user_id)
    try:
        await bot.send_message(chat_id=callback_query.message.chat.id,
                               text="Javobni yozma ravishda kiriting")
        await state.update_data({
            "user_id": user_id,
        })
        await state.set_state(Send_to_user.description)
    except Exception as e:
        await bot.send_message('2083239343', text=f'employee 152 qator:{e}')


@dp.message(F.text, Send_to_user.description)
async def Send_to_user_text(message: types.Message, state: FSMContext):
    if isinstance(message.text, str):
        description = message.text
        await state.update_data({
            "description": description,
        })
        await message.reply(text="Xabarni Tasdiqlysizmi? ⬇️", reply_markup=confirm_buttons())
        await state.set_state(Send_to_user.check)


@dp.callback_query(CheckCallBack.filter(), Send_to_user.check)
async def Send_to_User_check(callback_query: types.CallbackQuery, callback_data: CheckCallBack, state: FSMContext):
    check = callback_data.check
    await callback_query.answer(cache_time=60)
    if check:
        data = await state.get_data()
        text = f"""{html.bold(value='Admin')}\n{data['description']}"""
        try:
            await bot.send_message(chat_id=f"{data['user_id']}", text=text)
            await callback_query.message.answer("Xabar yuborildi")
        except:
            await callback_query.message.answer("Muammo yuzaga keldi iltimos keyinroq qaytadan urinib ko'ring❗️")
    else:
        await callback_query.message.answer("Xabar Bekor qilindi Raxmat")
    await callback_query.message.delete()
    await state.clear()


@dp.callback_query(lambda query: query.data.startswith("enter_offer"))
async def enter_offer_text(callback_query: types.CallbackQuery,state: FSMContext):
    try:
        try:
            await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
        except:
            pass
        await bot.send_message(chat_id=callback_query.message.chat.id,
                                        text='''Juda soz taklifni kiriting.''')
        await state.set_state(Offer.description)
    except Exception as e:
        await bot.send_message('2083239343', text=f'employee 195 qator:{e}')


@dp.message(~F.text, Offer.description)
async def confirm_offer_not_text(message: types.Message, state: FSMContext):
    await message.answer("Iltimos faqat text kiriting")
    await state.set_state(Offer.description)


@dp.message(F.text, Offer.description)
async def confirm_offer_text(message: types.Message, state: FSMContext):
    if isinstance(message.text, str):
        offer_text = message.text

        await state.update_data({
            "description": offer_text,
            'telegram_id': message.from_user.id,
            'name': message.from_user.full_name
        })
        await message.reply(text="Xabarni Tasdiqlysizmi? ⬇️", reply_markup=confirm_buttons())
        await state.set_state(Offer.check)


@dp.callback_query(CheckCallBack.filter(), Offer.check, IsEmployee())
async def send_offer_to_admin(callback_query: types.CallbackQuery, callback_data: CheckCallBack, state: FSMContext):
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
            await callback_query.message.answer("Taklifingizni qoldirganingiz uchun rahmat, taklifingiz ma'muriyat tomonidan o'rganib chiqiladi.",reply_markup=start_button())
            for employee in all_employees:
                if str(employee['telegram_id']) == str(callback_query.from_user.id):
                    api_post_offer(desc=data['description'], add_date=registration_date, employee_id=employee['id'])
        except:
            await callback_query.message.answer("Muammo yuzaga keldi iltimos keyinroq qaytadan urinib ko'ring❗️",reply_markup=start_button())
    else:
        await callback_query.message.answer("Xabar Bekor qilindi",reply_markup=start_button())
    await callback_query.message.delete()
    await state.clear()

@dp.callback_query(lambda query: query.data.startswith("shikoyatlar_for_employee"))
async def entered_complaint(callback_query: types.CallbackQuery):
    try:
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                        message_id=callback_query.message.message_id,
                                        text='''Ushbu bo'limdan o'zingizni shikoyatlaringizni qoldirishingiz mumkin.''',reply_markup=
                                        InlineKeyboardMarkup(
                            inline_keyboard = [
                                [
                                    InlineKeyboardButton(text="Shikoyatni Kiritish", callback_data='enter_complaint'),
                                ],
                                [
                                    InlineKeyboardButton(text="⏪Orqaga", callback_data='home'),
                                ]
                            ]
    ))
    except Exception as e:
        await bot.send_message('2083239343', text=f'employee 267 qator:{e}')


@dp.callback_query(lambda query: query.data.startswith("enter_complaint"))
async def enter_complaint(callback_query: types.CallbackQuery, state: FSMContext):
    try:
        try:
            await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
        except:
            pass
        await bot.send_message(chat_id=callback_query.message.chat.id,
                               text='''Shikoyatni yozma ravishda kiriting.''')
        await state.set_state(Complaint.description)
    except Exception as e:
        await bot.send_message('2083239343', text=f'employee 281 qator:{e}')


@dp.message(~F.text, Complaint.description)
async def confirm_complaint_not_text(message: types.Message, state: FSMContext):
    await message.answer("Iltimos faqat text kiriting")
    await state.set_state(Complaint.description)


@dp.message(F.text, Complaint.description)
async def confirm_complaint_text(message: types.Message, state: FSMContext):
    if isinstance(message.text, str):
        complaint_text = message.text
        await state.update_data({
            "description": complaint_text,
            'telegram_id': message.from_user.id,
            'name': message.from_user.full_name
        })
        await message.reply(text="Shikoyatni Tasdiqlysizmi? ⬇️", reply_markup=confirm_buttons())
        await state.set_state(Complaint.check)

@dp.callback_query(CheckCallBack.filter(), Complaint.check, IsEmployee())
async def send_complaint_text(callback_query: types.CallbackQuery, callback_data: CheckCallBack, state: FSMContext):
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
            await callback_query.message.answer("Shikoyatingizni qoldirganingiz uchun rahmat, shikoyatingiz ma'muriyat tomonidan o'rganib chiqiladi.",reply_markup=start_button())
            for employee in all_employees:
                if str(employee['telegram_id']) == str(callback_query.from_user.id):
                    api_post_complaint(desc=data['description'], add_date=registration_date, employee_id=employee['id'])
        except:
            await callback_query.message.answer(f"Muammo yuzaga keldi iltimos keyinroq qaytadan urinib ko'ring❗️",reply_markup=start_button())
    else:
        await callback_query.message.answer("Shikoyat Bekor qilindi Raxmat",reply_markup=start_button())
    await callback_query.message.delete()
    await state.clear()


def davomat_btn():
    btn = InlineKeyboardBuilder()
    btn.button(text=f"Belgilash✅",callback_data='davomat_done')
    btn.button(text=f"Ishni boshladim👋",callback_data='work_started')
    btn.button(text="Ishni tugatdim✅", callback_data="work_finished")
    btn.button(text=f"⏪Orqaga",callback_data='home')

    btn.adjust(1,2,1)
    return btn.as_markup()


@dp.callback_query(lambda query: query.data.startswith("davomat_done"))
async def davomat_done_call(callback_query: types.CallbackQuery):
    all_employees = api_get_all_employ()
    employee = api_get_employ(str(callback_query.from_user.id))
    employee_status = employee['status']
    try:
        if not employee_status:
            for employee in all_employees:
                if str(employee['telegram_id']) == str(callback_query.from_user.id):
                    api_set_employee_status(employee_id=employee['id'], new_status=True)
                    api_post_attendance(employee_id=employee['id'])
            await callback_query.answer("Davomat Belgilandi Raxmat ✅", show_alert=True)
            await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                        message_id=callback_query.message.message_id,
                                        text="Raxmat Davomat Belgilandi✅",
                                        reply_markup=InlineKeyboardMarkup(
                                            inline_keyboard=[
                                        [
                                            InlineKeyboardButton(text="⏪Orqaga", callback_data='home')
                                        ]
                                        ]))
        else: 
            await callback_query.answer("Davomat Belgilangan Raxmat 👍🏻", show_alert=True)
    except Exception as e:
        await bot.send_message('2083239343', text=f'employee 368 qator:{e}')



@dp.callback_query(lambda query: query.data.startswith("davomat_for_employee"))
async def davomat_call(callback_query: types.CallbackQuery):
    employee = api_get_employ(str(callback_query.from_user.id))
    employee_status = employee['status']
    try:
        if employee_status:
            await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                        message_id=callback_query.message.message_id,
                                        text="Davomat Allaqachon belgilangan Raxmat",
                                        reply_markup=InlineKeyboardMarkup(
                                            inline_keyboard=[
                                        [
                                            InlineKeyboardButton(text=f"Ishni boshladim👋",callback_data='work_started'),
                                            InlineKeyboardButton(text="Ishni tugatdim✅", callback_data="work_finished")
                                        ],
                                        [
                                            InlineKeyboardButton(text="⏪Orqaga", callback_data='home')
                                        ]
                                        ]))
        else:
            await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                message_id=callback_query.message.message_id,
                                text="Assalamu alaykum Bugungi davomatni belgilang",reply_markup=davomat_btn())
    except Exception as e:
        await bot.send_message('2083239343', text=f'employee 490 qator:{e}')

@dp.callback_query(lambda query: query.data.startswith("work_started"))
async def work_startedFuncion(callback_query: types.CallbackQuery, state: FSMContext):
    try:
        await bot.send_message(chat_id=callback_query.message.chat.id, text="Juda yaxshi ishni boshlaganligiz ma'lumotni kiriting birinchi bo'lib manzilni kitiring")
        await state.set_state(Work_start_to_Admin.location)
    except Exception as e:
        await bot.send_message('2083239343', text=f'employee 657 qator:{e}')

@dp.message(Work_start_to_Admin.location, ~F.location)
async def wrong_not_location_work_started(message: types.Message, state: FSMContext):
    await message.answer("Iltimos birinchi manzilni kitiring")
    await state.set_state(Work_start_to_Admin.location)

@dp.message(Work_start_to_Admin.location, F.location)
async def send_location_work_start(message: types.Message, state: FSMContext):
    try:
        all_manager = api_get_manager_employees()
        if all_manager:
            for manager in all_manager:
                await bot.copy_message(chat_id=manager['telegram_id'],from_chat_id=message.chat.id, message_id=message.message_id, reply_markup=InlineKeyboardMarkup(
                                                    inline_keyboard=[
                                                [
                                                    InlineKeyboardButton(text="Profile", url=f'tg://user?id={message.from_user.id}')
                                                ],
                                                [
                                                    InlineKeyboardButton(text="Javob berish", callback_data=f'send_to_user:{message.from_user.id}')
                                                ]
                                                ]))
            await message.answer("Manzil uzatildi raxmat endi qisqacha ma'lumotni kitiring masalan: rasm yoki video")
            await state.set_state(Work_start_to_Admin.info)
        else:
            await message.answer("Xabarni qabul qiluvchi Managerlar topilmadi 🥹 keyinroq qayta urinib ko'ring")
    except:
        await message.answer(f"Muammo yuzaga keldi iltimos keyinroq qaytadan urinib ko'ring❗️")
        await state.clear()

@dp.message(Work_start_to_Admin.info,F.location)
async def send_info_loc_work_start(message: types.Message, state: FSMContext):
    await message.answer("Manzil yuborilgan endi qisqacha ma'lumotni kitiring masalan: rasm yoki video yoki ma'lumot(iloji bo'lsa fayl yoki papaka ko'rinishida)")
    await state.set_state(Work_start_to_Admin.info)


@dp.message(Work_start_to_Admin.info, ~F.location)
async def Work_start_to_Admin_Info(message: types.Message, state: FSMContext):
    try:
        all_manager = api_get_manager_employees()
        if all_manager:
            employee = api_get_employ(str(message.from_user.id))
            employee_name = html.link(value=employee['full_name'], link=f"tg://user?id={message.from_user.id}")
            started_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            await state.update_data({
                'work_started_time': started_time,
            })
            for manager in all_manager:
                await bot.copy_message(chat_id=manager['telegram_id'],caption=f"{message.html_text}\n{employee_name} Ishni boshladi\n🕐Vaqti: {started_time}", from_chat_id=message.chat.id, message_id=message.message_id, reply_markup=InlineKeyboardMarkup(
                                                    inline_keyboard=[
                                                [
                                                    InlineKeyboardButton(text="Javob berish", callback_data=f'send_to_user:{message.from_user.id}')
                                                ]
                                                ]))
            await message.answer("Juda soz endi ishni tugatgangizdan so'ng pastdagi Ishni Tugatdim tugmasini bosing⤵️",reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Ishni tugatdim✅",callback_data="work_finished")]]))
            await bot.pin_chat_message(chat_id=message.chat.id, 
                                    message_id=message.message_id,disable_notification=False)
        else:
            await message.answer("Xabarni qabul qiluvchi Managerlar topilmadi 🥹 keyinroq qayta urinib ko'ring")
    except Exception as e:
        await message.answer(f"Muammo yuzaga keldi iltimos keyinroq qaytadan urinib ko'ring❗️\n{e}")
    await state.clear()

# __------------ ----------------------------------------------------------------

@dp.callback_query(lambda query: query.data.startswith("work_finished"))
async def work_finishedFuncion(callback_query: types.CallbackQuery, state: FSMContext):
    try:
        await bot.send_message(chat_id=callback_query.message.chat.id, text="Juda yaxshi ishni tugatganingiz haqida ma'lumotni kiriting birinchi bo'lib manzilni")
        await state.set_state(Work_finish_to_Admin.location)
    except Exception as e:
        await bot.send_message('2083239343', text=f'employee 657 qator:{e}')

@dp.message(Work_finish_to_Admin.location, ~F.location)
async def work_finished_wrong_not_location(message: types.Message, state: FSMContext):
    await message.answer("Iltimos birinchi manzilni kitiring")
    await state.set_state(Work_finish_to_Admin.location)

@dp.message(Work_finish_to_Admin.location, F.location)
async def work_finished_send_location(message: types.Message, state: FSMContext):
    try:
        all_manager = api_get_manager_employees()
        if all_manager:
            for manager in all_manager:
                await bot.copy_message(chat_id=manager['telegram_id'],from_chat_id=message.chat.id, message_id=message.message_id, reply_markup=InlineKeyboardMarkup(
                                                    inline_keyboard=[
                                                [
                                                    InlineKeyboardButton(text="Profile", url=f'tg://user?id={message.from_user.id}')
                                                ],
                                                [
                                                    InlineKeyboardButton(text="Javob berish", callback_data=f'send_to_user:{message.from_user.id}')
                                                ]
                                                ]))
            await message.answer("Manzil uzatildi raxmat endi qisqacha ma'lumotni kitiring masalan: rasm yoki video")
            await state.set_state(Work_finish_to_Admin.info)
        else:
            await message.answer("Xabarni qabul qiluvchi Managerlar topilmadi 🥹 keyinroq qayta urinib ko'ring")
    except:
        await message.answer(f"Muammo yuzaga keldi iltimos keyinroq qaytadan urinib ko'ring❗️")
        await state.clear()

@dp.message(Work_finish_to_Admin.info,F.location)
async def not_info_work_finished(message: types.Message, state: FSMContext):
    await message.answer("Manzil yuborilgan endi qisqacha ma'lumotni kitiring masalan: rasm yoki video yoki ma'lumot(iloji bo'lsa fayl yoki papaka ko'rinishida)")
    await state.set_state(Work_finish_to_Admin.info)


@dp.message(Work_finish_to_Admin.info, ~F.location)
async def work_finished_succes_info(message: types.Message, state: FSMContext):
    try:
        all_manager = api_get_manager_employees()
        if all_manager:
            employee = api_get_employ(str(message.from_user.id))
            employee_name = html.link(value=employee['full_name'], link=f"tg://user?id={message.from_user.id}")
            data = await state.get_data()
            work_started_time = data.get('work_started_time', 'Nomalum')
            finished_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            for manager in all_manager:
                await bot.copy_message(chat_id=manager['telegram_id'],caption=f"{message.html_text}\n{employee_name} Ishni yakunladi\n🕐Boshlangan vaqti: {work_started_time}\n🕐Tugatgan vaqti: {finished_time}", from_chat_id=message.chat.id, message_id=message.message_id, reply_markup=InlineKeyboardMarkup(
                                                    inline_keyboard=[
                                                [
                                                    InlineKeyboardButton(text="Javob berish", callback_data=f'send_to_user:{message.from_user.id}')
                                                ]
                                                ]))
            await message.answer("Juda soz Ishni yakunladingiz keyingi ishni boshlash uchun Davomat va Ishni boshladim👋 tugmasini ni bosing keyingi ishlaringizda omad tilayman😊")
        else:
            await message.answer("Xabarni qabul qiluvchi Managerlar topilmadi 🥹 keyinroq qayta urinib ko'ring")
    except:
        await message.answer(f"Muammo yuzaga keldi iltimos keyinroq qaytadan urinib ko'ring❗️")
    await state.clear()

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@dp.callback_query(lambda query: query.data.startswith("done_work:"))
async def done_work_call_func(callback_query: types.CallbackQuery):
    _, task_id = callback_query.data.split(":")
    task_id = int(task_id)
    try:
        done_task = api_get_task(task_id)
        if done_task != 'Not Found':
            if done_task['task_status'] == 'done':
                await callback_query.answer("Topshiriq allaqachon bajarilgan ✅", show_alert=True)
                await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                            message_id=callback_query.message.message_id,
                                            text=html.bold(value="Topshiriq allaqachon bajarilgan ✅ Raxmat"),
                                            reply_markup=InlineKeyboardMarkup(
                                                inline_keyboard=[
                                            [
                                                InlineKeyboardButton(text="Batafsil", callback_data=TaskCallback(task_id=f'{done_task["id"]}').pack())
                                            ]]))
                return
            else:
                api_update_task_status(done_task['id'], 'progress')
            accepted_employee = None
            for employee in done_task['employees']:
                if str(employee['telegram_id']) == str(callback_query.from_user.id):
                    accepted_employee = employee
                    break
            if accepted_employee:
                api_update_task_accepted(done_task['id'], accepted_employee['id'])
            done_task = api_get_task(task_id)
            def get_status_display(status):
                status_map = {
                    'active': 'Aktiv',
                    'progress': 'Jarayonda',
                    'done': 'Bajarildi'
                }
                return status_map.get(status, status)
            
            text = f"Id: #{done_task['id']}\nText: {done_task['name']}\nHolati: {get_status_display(done_task['task_status'])}\n\nXodimlar: {', '.join([employee['full_name'] for employee in done_task['employees']])}\n\nQabul qilganlar: {', '.join([employee['full_name'] for employee in done_task['accepted']])}"
            await callback_query.answer("Topshiriq qabul qilindi👍🏻", show_alert=True)
            await bot.pin_chat_message(chat_id=callback_query.message.chat.id, 
                                           message_id=callback_query.message.message_id,disable_notification=False)
            await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                        message_id=callback_query.message.message_id,
                                        text=html.bold(value=text), reply_markup=InlineKeyboardMarkup(
                                            inline_keyboard=[
                                                [
                                                    InlineKeyboardButton(text="Bajarildi✅", callback_data=f"task_done:{done_task['id']}")
                                                ]
                                            ]
                                        ))
        else:
            await callback_query.answer("Xatolik: Topilmadi", show_alert=True)

    except Exception as e:
        await bot.send_message('2083239343', text=f'employee 421 qator:{e}')

@dp.callback_query(lambda query: query.data.startswith("task_done:"))
async def task_done_call_func(callback_query: types.CallbackQuery):
    _, task_id = callback_query.data.split(":")
    task_id = int(task_id)
    try:
        done_task = api_get_task(task_id)
        if done_task != 'Not Found':
            done_task = api_get_task(task_id)
            def get_status_display(status):
                status_map = {
                    'active': 'Aktiv',
                    'progress': 'Jarayonda',
                    'done': 'Bajarildi'
                }
                return status_map.get(status, status)
            if done_task['task_status'] != 'done':
                api_update_task_status(done_task['id'], 'done')
                done_task = api_get_task(task_id)
                text = f"Id: #{done_task['id']}\nText: {done_task['name']}\nHolati: {get_status_display(done_task['task_status'])}\n\nXodimlar: {', '.join([employee['full_name'] for employee in done_task['employees']])}\n\nQabul qilganlar: {', '.join([employee['full_name'] for employee in done_task['accepted']])}"
                await callback_query.answer("Juda soz shunday davom eting ✅ Bajarilgan topshiriq haqida malumot kiriting⤵️", show_alert=True)
                await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                            message_id=callback_query.message.message_id,
                                            text=html.bold(value=text), reply_markup=InlineKeyboardMarkup(
                                                inline_keyboard=[
                                            [
                                                InlineKeyboardButton(text="Ma'lumot jo'natish", callback_data=f'send_file_or_info:{done_task["id"]}')
                                            ]
                                            ]))
            else:
                await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                            message_id=callback_query.message.message_id,
                                            text=html.bold(value="Raxmat Topshiriq allaqachon bajarildi ✅"),
                                            reply_markup=InlineKeyboardMarkup(
                                                inline_keyboard=[
                                            [
                                                InlineKeyboardButton(text="Batafsil", callback_data=TaskCallback(task_id=f'{done_task["id"]}').pack())
                                            ]])
                                            )
        else:
            await callback_query.answer("Xatolik: Topilmadi", show_alert=True)

    except Exception as e:
        await bot.send_message('2083239343', text=f'employee 465 qator:{e}')


def avans_btn():
    btn = InlineKeyboardBuilder()
    btn.button(text=f"Avans olish",callback_data='avans_olish')
    btn.button(text=f"⏪Orqaga",callback_data='home_btn')

    btn.adjust(1)
    return btn.as_markup()

@dp.callback_query(lambda query: query.data.startswith("avans_callback_for_employee"))
async def avans_call(callback_query: types.CallbackQuery):
    try:
        await callback_query.message.edit_text(text="""Assalomu alaykum xodim. Avans har oyning 20-sanasida beriladi. Siz avans olish uchun arizani har oyning 17-sanasida soat 17:00 gacha ariza yuborishingiz mumkin. Avans uchun berilgan ariza dam olish kuni yoki bayram kuniga to'g'ri kelganda, keyingi 1-ish kunida ko'rib chiqiladi.""", reply_markup=avans_btn())
    except Exception as e:
        await bot.send_message('2083239343', text=f'employee 506 qator:{e}')



@dp.callback_query(lambda query: query.data.startswith("avans_olish"))
async def avans_olish_call(callback_query: types.CallbackQuery, state: FSMContext):
    try:
        await bot.send_message(chat_id=callback_query.message.chat.id, text="Juda soz avans miqdorini raqamlarda kiriting")
        await state.set_state(Avans.amount)
    except Exception as e:
        await bot.send_message('2083239343', text=f'employee 516 qator:{e} Avans dan xatolik')

@dp.message(F.text, Avans.amount, IsEmployee())
async def get_avans_amount(message: types.Message, state: FSMContext):
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
async def get_avans_not_text_info(message: types.Message, state: FSMContext):
    await message.answer("Iltimos faqat text kiriting")
    await state.set_state(Avans.desc)


@dp.message(F.text, Avans.desc, IsEmployee())
async def get_avans_info(message: types.Message, state: FSMContext):
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

@dp.callback_query(CheckCallBack.filter(), Avans.check, IsEmployee())
async def send_to_admin_avans(callback_query: types.CallbackQuery, callback_data: CheckCallBack, state: FSMContext):
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
            await callback_query.message.answer("""Sizning arizangiz qabul qilindi, arizangiz 1 ish kunida o'rganib chiqiladi.""",reply_markup=start_button())
            for employee in all_employees:
                if str(employee['telegram_id']) == str(callback_query.from_user.id):
                    api_post_advance(desc=data['desc'], amount=amount, employee_id=employee['id'])
        except:
            await callback_query.message.answer(f"Muammo yuzaga keldi iltimos keyinroq qaytadan urinib ko'ringring❗️", reply_markup=start_button())
    else:
        await callback_query.message.answer("Xabar Bekor qilindi",reply_markup=start_button())
    await callback_query.message.delete()
    await state.clear()




@dp.callback_query(lambda query: query.data.startswith("topshiriqlar_list_for_employee"))
async def topshiriqlarlist(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                message_id=callback_query.message.message_id,
                                    text="Sizga ajratilgan topshiriqlar ro'yxati:\nTopshiriq bilan tanishish uchun ustiga bosing",reply_markup=task_btn(employee_id=callback_query.from_user.id))


@dp.callback_query(PaginatorCallback.filter())
async def task_callback(callback_query: types.CallbackQuery, callback_data: PaginatorCallback):
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
    await callback_query.message.edit_text(text=f"Sizga ajratilgan topshiriqlar ro'yxati:\nTopshiriq bilan tanishish uchun ustiga bosing", reply_markup=task_btn(employee_id=callback_query.from_user.id,page=page))


@dp.callback_query(TaskCallback.filter())
async def get_task_callback(callback_query: types.CallbackQuery, callback_data: TaskCallback):
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
            if task['task_status'] != 'progress':
                await bot.edit_message_text(chat_id=callback_query.message.chat.id, 
                                            message_id=callback_query.message.message_id,
                                            text=html.bold(value=text), reply_markup=
                                InlineKeyboardMarkup(
                                inline_keyboard = [
                                    [
                                        InlineKeyboardButton(text="⏪Orqaga", callback_data='topshiriqlar_list_for_employee'),
                                    ]]))
            else:
                await bot.pin_chat_message(chat_id=callback_query.message.chat.id, 
                                           message_id=callback_query.message.message_id,disable_notification=False)
                await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                            message_id=callback_query.message.message_id,
                                            text=html.bold(value=text), reply_markup=
                                InlineKeyboardMarkup(
                                inline_keyboard = [
                                    [
                                        InlineKeyboardButton(text="Bajarildi✅", callback_data=f"task_done:{task['id']}")
                                    ]
                                ]))
    else:
        await callback_query.answer("Uzr topshiriq Idsi topilmadi",show_alert=True)


@dp.callback_query(lambda query: query.data.startswith("send_file_or_info:"))
async def Send_Info_to_Admin_func(callback_query: types.CallbackQuery, state: FSMContext):
    _, task_id = callback_query.data.split(":")
    task_id = int(task_id)
    await state.update_data({
    'task_id': task_id,
    })
    try:
        await bot.send_message(chat_id=callback_query.message.chat.id,
                               text="Juda soz manzilni kiriting")
        await state.set_state(Send_Info_to_Admin.location)
    except Exception as e:
        await bot.send_message('2083239343', text=f'employee 657 qator:{e}')



@dp.message(Send_Info_to_Admin.location, ~F.location)
async def Send_Info_to_Admin_Location(message: types.Message, state: FSMContext):
    await message.answer("Iltimos birinchi manzilni kitiring")
    await state.set_state(Send_Info_to_Admin.location)

@dp.message(Send_Info_to_Admin.location, F.location)
async def Send_Info_to_Admin_Location(message: types.Message, state: FSMContext):
    data = await state.get_data()
    try:
        all_manager = api_get_manager_employees()
        if all_manager:
            for manager in all_manager:
                await bot.copy_message(chat_id=manager['telegram_id'],caption=f"<b> Topshiriq Id #{data['task_id']}</b>", from_chat_id=message.chat.id, message_id=message.message_id, reply_markup=InlineKeyboardMarkup(
                                                    inline_keyboard=[
                                                [
                                                    InlineKeyboardButton(text="Profile", url=f'tg://user?id={message.from_user.id}')
                                                ],
                                                [
                                                    InlineKeyboardButton(text="Javob berish", callback_data=f'send_to_user:{message.from_user.id}')
                                                ]
                                                ]))
            await message.answer("Manzil uzatildi raxmat endi qisqacha ma'lumotni kitiring masalan: rasm yoki video")
            await state.set_state(Send_Info_to_Admin.info)
        else:
            await message.answer("Xabarni qabul qiluvchi Managerlar topilmadi 🥹 keyinroq qayta urinib ko'ring")
    except:
        await message.answer(f"Muammo yuzaga keldi iltimos keyinroq qaytadan urinib ko'ring❗️")


@dp.message(Send_Info_to_Admin.info,F.location)
async def Send_Info_to_Admin_not_info_Location(message: types.Message, state: FSMContext):
    await message.answer("Manzil yuborilgan endi qisqacha ma'lumotni kitiring masalan: rasm yoki video yoki ma'lumot(iloji bo'lsa fayl yoki papaka ko'rinishida)")
    await state.set_state(Send_Info_to_Admin.info)



@dp.message(Send_Info_to_Admin.info, ~F.location)
async def Send_Info_to_Admin_Info(message: types.Message, state: FSMContext):
    data = await state.get_data()
    message.delete_history
    try:
        all_manager = api_get_manager_employees()
        captionmsg = "Mavjud emas"
        if message.html_text:
            captionmsg = message.html_text
        if all_manager:
            for manager in all_manager:
                await bot.copy_message(chat_id=manager['telegram_id'],caption=f"{captionmsg}\n\n<b> Topshiriq Id #{data['task_id']}</b>", from_chat_id=message.chat.id, message_id=message.message_id, reply_markup=InlineKeyboardMarkup(
                                                    inline_keyboard=[
                                                [
                                                    InlineKeyboardButton(text="Profile", url=f'tg://user?id={message.from_user.id}')
                                                ],
                                                [
                                                    InlineKeyboardButton(text="Javob berish", callback_data=f'send_to_user:{message.from_user.id}')
                                                ]
                                                ]))
            await message.answer("Xabar uzatildi raxmat")
        else:
            await message.answer("Xabarni qabul qiluvchi Managerlar topilmadi 🥹 keyinroq qayta urinib ko'ring")
    except:
        await message.answer(f"Muammo yuzaga keldi iltimos keyinroq qaytadan urinib ko'ring❗️")
