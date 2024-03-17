from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton,WebAppInfo
from aiogram.filters.callback_data import CallbackData
from api import get_all_task, get_all_employee,get_all_advance
page_size = 2


class CheckCallBack(CallbackData, prefix='ikb1'):
    check:bool

def confirm_buttons():
    button = InlineKeyboardBuilder()
    button.button(text="Tasdiqlash✅", callback_data=CheckCallBack(check=True))
    button.button(text="Bekor qilish🚫", callback_data=CheckCallBack(check=False))
    button.adjust(1)

    return button.as_markup()


class PaginatorCallback(CallbackData, prefix='page1'):
    page: int
    action:str
    length:int

class TaskCallback(CallbackData, prefix='task1'):
    task_id: int


class ForAdminPaginatorCallback(CallbackData, prefix='page2'):
    page: int
    action:str
    length:int
    status:str

class ForAdminTaskCallback(CallbackData, prefix='task2'):
    task_id: int

class ForManagerPaginatorCallback(CallbackData, prefix='page5'):
    page: int
    action:str
    length:int
    status:str

class ForManagerTaskCallback(CallbackData, prefix='task3'):
    task_id: int

class EmployeeListPaginatorCallback(CallbackData, prefix='page3'):
    page: int
    action:str
    length:int

class AttendancePaginatorCallback(CallbackData, prefix='page4'):
    page: int
    action:str
    length:int


class AdvancePaginatorCallback(CallbackData, prefix='advance1'):
    page: int
    action:str
    length:int

class AdvanceCallback(CallbackData, prefix='advance'):
    advance_id: int


def get_task(id):
    for topshiriq in get_all_task():
        if topshiriq['id'] == id:
            return topshiriq
    return None


def task_btn(employee_id,page:int=0):

    def filter_tasks_by_employee_id(telegram_id):
        all_tasks = get_all_task()
        filtered_tasks = []
        for task in all_tasks:
            for employee in task['employees']:
                if employee['telegram_id'] == str(telegram_id):
                    filtered_tasks.append(task)
                    break
        return filtered_tasks

    btn = InlineKeyboardBuilder()
    filtered_tasks = filter_tasks_by_employee_id(telegram_id=employee_id)
    length = len(filtered_tasks)
    data = filtered_tasks

    try:
        start = page*page_size
        finish = (page+1)*page_size
        if finish>length:
            datas = data[start:length]
        else:
            datas = data[start:finish]
    except:
        pass

    if datas:
        for task in datas:
            btn.row(InlineKeyboardButton(text=f"Topshiriq: {task['id']}", callback_data=TaskCallback(task_id=task['id']).pack()), width=2)
        btn.row(InlineKeyboardButton(text="Bosh sahifa🏠", callback_data='home'))
        if page > 0:
            btn.row(
                InlineKeyboardButton(
                    text=f"⏪Orqaga", callback_data=PaginatorCallback(page=page, action='prev', length=length).pack()
                )
            )
        if page > 0 and finish < length:
            if page_size > 0:
                btn.row(InlineKeyboardButton(text=f"{page+1} of {length//page_size+1}", callback_data='sahifa'))

        if finish < length:
            btn.row(
                InlineKeyboardButton(
                    text=f"⏭️Oldinga", callback_data=PaginatorCallback(page=page, action='next', length=length).pack()
                )
            )

        if page > 0 and finish < length:
            if page_size > 0:
                btn.adjust(*(tuple(1 for _ in range(page_size+1)) + (3,)))

        return btn.as_markup()
    else:
        btn.row(InlineKeyboardButton(text="Topilmadi", callback_data='home'))
        return btn.as_markup()

# task btn for employee done


def get_task_status(status):
    all_task = get_all_task()
    filter_task = [task for task in all_task if task.get('task_status') == str(status)]
    return filter_task

STATUS_CHOICES = {
    'active': 'Aktiv',
    'progress': 'Jarayonda',
    'done': 'Bajarildi'
}
def filter_tasks_by_status_btns():
    btn = InlineKeyboardBuilder()
    status_buttons = []
    for status_key, status_label in STATUS_CHOICES.items():
        status_buttons.append(InlineKeyboardButton(
            text=status_label,
            callback_data=f"filter_by_status_{status_key}"
        ))
    
    btn.add(*status_buttons)
    btn.adjust(1)

    return btn.as_markup()

def tasks_btn_for_admin(status,page:int=0):
    btn = InlineKeyboardBuilder()
    filtered_tasks = get_task_status(status)
    length = len(filtered_tasks)
    data = filtered_tasks
    try:
        start = page*page_size
        finish = (page+1)*page_size
        if finish>length:
            datas = data[start:length]
        else:
            datas = data[start:finish]
    except:
        pass

    if datas:
        for task in datas:
            btn.row(InlineKeyboardButton(text=f"Topshiriq: {task['id']}", callback_data=ForAdminTaskCallback(task_id=task['id']).pack()), width=2)
        btn.row(InlineKeyboardButton(text="Bosh sahifa🏠", callback_data='back_to_home'))
        if page > 0:
            btn.row(
                InlineKeyboardButton(
                    text=f"⏪Orqaga", callback_data=ForAdminPaginatorCallback(status=status,page=page, action='prev', length=length).pack()
                )
            )
        if page > 0 and finish < length:
            if page_size > 0:
                btn.row(InlineKeyboardButton(text=f"{page+1} of {length//page_size+1}", callback_data="pagesforadmin"))


        if finish < length:
            btn.row(
                InlineKeyboardButton(
                    text=f"⏭️Oldinga", callback_data=ForAdminPaginatorCallback(status=status,page=page, action='next', length=length).pack()
                )
            )
        if page > 0 and finish < length:
            if page_size > 0:
                btn.adjust(*(tuple(1 for _ in range(page_size+1)) + (3,)))

        return btn.as_markup()
    else:
        btn.row(InlineKeyboardButton(text="Topilmadi", callback_data='back_to_home'))
        return btn.as_markup()
# For manager btn

def tasks_btn_for_manager(status ,page:int=0):
    btn = InlineKeyboardBuilder()
    filtered_tasks = get_task_status(status)
    length = len(filtered_tasks)
    data = filtered_tasks
    try:
        start = page*page_size
        finish = (page+1)*page_size
        if finish>length:
            datas = data[start:length]
        else:
            datas = data[start:finish]
    except:
        pass

    if datas:    
        for task in datas:
            btn.row(InlineKeyboardButton(text=f"Topshiriq: {task['id']}", callback_data=ForManagerTaskCallback(task_id=task['id']).pack()), width=2)
        btn.row(InlineKeyboardButton(text="Bosh sahifa🏠", callback_data='back_to_manager_home'))
        if page > 0:
            btn.row(
                InlineKeyboardButton(
                    text=f"⏪Orqaga", callback_data=ForManagerPaginatorCallback(status=status,page=page, action='prev', length=length).pack()
                )
            )
        if page > 0 and finish < length:
            if page_size > 0:
                btn.row(InlineKeyboardButton(text=f"{page+1} of {length//page_size+1}", callback_data="pagesforadmin"))


        if finish < length:
            btn.row(
                InlineKeyboardButton(
                    text=f"⏭️Oldinga", callback_data=ForManagerPaginatorCallback(status=status,page=page, action='next', length=length).pack()
                )
            )
        if page > 0 and finish < length:
            if page_size > 0:
                btn.adjust(*(tuple(1 for _ in range(page_size+1)) + (3,)))

        return btn.as_markup()
    else:
        btn.row(InlineKeyboardButton(text="Topilmadi", callback_data='back_to_manager_home'))
        return btn.as_markup()

# Employee

def employee_list_button(page:int=0):
    btn = InlineKeyboardBuilder()
    length = len(get_all_employee())
    data = get_all_employee()
    try:
        start = page*page_size
        finish = (page+1)*page_size
        if finish>length:
            datas = data[start:length]
        else:
            datas = data[start:finish]
    except:
        pass

    def get_status_display(status):
        status_map = {
            'admin': 'Admin',
            'manager': 'Manager',
            'student': 'Shogird',
            'worker': 'Ishchi'
        }
        return status_map.get(status, status)
    if datas:
        for employee in datas:
            btn.row(InlineKeyboardButton(text=f"{get_status_display(employee['position'])}-{employee['full_name']}",url=f"tg://user?id={employee['telegram_id']}"), width=2)
        btn.row(InlineKeyboardButton(text="Bosh sahifa🏠", callback_data='back_to_home'))
        if page > 0:
            btn.row(
                InlineKeyboardButton(
                    text=f"⏪Orqaga", callback_data=EmployeeListPaginatorCallback(page=page, action='prev', length=length).pack()
                )
            )
        if page > 0 and finish < length:
            if page_size > 0:
                btn.row(InlineKeyboardButton(text=f"{page+1} of {length//page_size+1}", callback_data="pagesforadmin"))


        if finish < length:
            btn.row(
                InlineKeyboardButton(
                    text=f"⏭️Oldinga", callback_data=EmployeeListPaginatorCallback(page=page, action='next', length=length).pack()
                )
            )

        if page > 0 and finish < length:
            if page_size > 0:
                btn.adjust(*(tuple(1 for _ in range(page_size+1)) + (3,)))

        return btn.as_markup()
    else:
        btn.row(InlineKeyboardButton(text="Topilmadi", callback_data='back_to_home'))
        return btn.as_markup()
    
# def attendance_button():
#     filter_employees = [employee for employee in get_all_employee() if employee['status']]


def attendance_button(page:int=0):
    btn = InlineKeyboardBuilder()
    filter_employees = [employee for employee in get_all_employee() if employee['status']]
    length = len(filter_employees)
    data = filter_employees
    try:
        start = page*page_size
        finish = (page+1)*page_size
        if finish>length:
            datas = data[start:length]
        else:
            datas = data[start:finish]
    except:
        pass

    if datas:
        for employee in datas:
            btn.row(InlineKeyboardButton(text=f"{employee['full_name']}",url=f"tg://user?id={employee['telegram_id']}"), width=2)
        btn.row(InlineKeyboardButton(text="Bosh sahifa🏠", callback_data='back_to_home'))
        if page > 0:
            btn.row(
                InlineKeyboardButton(
                    text=f"⏪Orqaga", callback_data=AttendancePaginatorCallback(page=page, action='prev', length=length).pack()
                )
            )
        if page > 0 and finish < length:
            if page_size > 0:
                btn.row(InlineKeyboardButton(text=f"{page+1} of {length//page_size+1}", callback_data="pagesforadmin"))

        if finish < length:
            btn.row(
                InlineKeyboardButton(
                    text=f"⏭️Oldinga", callback_data=AttendancePaginatorCallback(page=page, action='next', length=length).pack()
                )
            )

        if page > 0 and finish < length:
            if page_size > 0:
                btn.adjust(*(tuple(1 for _ in range(page_size+1)) + (3,)))

        return btn.as_markup()
    else:
        btn.row(InlineKeyboardButton(text="Topilmadi", callback_data='back_to_home'))
        return btn.as_markup()


def get_advance(id):
    for advance in get_all_advance():
        if advance['id'] == id:
            return advance
    return None


def advance_btn_for_admin(page:int=0):
    btn = InlineKeyboardBuilder()
    length = len(get_all_advance())
    data = get_all_advance()
    try:
        start = page*page_size
        finish = (page+1)*page_size
        if finish>length:
            datas = data[start:length]
        else:
            datas = data[start:finish]
    except:
        pass

    if datas:    
        for avans in datas:
            btn.row(InlineKeyboardButton(text=f"Avans: {avans['id']}", callback_data=AdvanceCallback(advance_id=avans['id']).pack()), width=2)
        btn.row(InlineKeyboardButton(text="Bosh sahifa🏠", callback_data='back_to_home'))
        if page > 0:
            btn.row(
                InlineKeyboardButton(
                    text=f"⏪Orqaga", callback_data=AdvancePaginatorCallback(page=page, action='prev', length=length).pack()
                )
            )
        if page > 0 and finish < length:
            if page_size > 0:
                btn.row(InlineKeyboardButton(text=f"{page+1} of {length//page_size+1}" , callback_data='pageOf'))


        if finish < length:
            btn.row(
                InlineKeyboardButton(
                    text=f"⏭️Oldinga", callback_data=AdvancePaginatorCallback(page=page, action='next', length=length).pack()
                )
            )

        if page > 0 and finish < length:
            if page_size > 0:
                btn.adjust(*(tuple(1 for _ in range(page_size+1)) + (3,)))

        return btn.as_markup()
    else:
        btn.row(InlineKeyboardButton(text="Topilmadi", callback_data='back_to_home'))
        return btn.as_markup()