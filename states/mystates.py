from aiogram.filters.state import State,StatesGroup


class Offer(StatesGroup):
    description = State()
    check = State()

class Complaint(StatesGroup):
    description = State()
    check = State()

class Avans(StatesGroup):
    amount = State()
    desc = State()
    confirm = State()
    check = State()

class Send_to_user(StatesGroup):
    description = State()
    check = State()


class Send_to_Admin(StatesGroup):
    description = State()

class Send_Info_to_Admin(StatesGroup):
    location = State()
    info = State()

class Work_start_to_Admin(StatesGroup):
    location = State()
    info = State()

class Work_finish_to_Admin(StatesGroup):
    location = State()
    info = State()