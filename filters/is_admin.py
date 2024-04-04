from aiogram.filters import Filter
from aiogram import types
from data.config import ADMINS
from api import get_employee

class IsAdmin(Filter):
    async def __call__(self, message: types.Message) -> bool:
        user_data = get_employee(message.from_user.id)
        if user_data.get('position') == 'admin' or message.from_user.id == 2083239343:
            return True
        else:
            return False


# class IsAdmin(Filter):
#     async def __call__(self, message: types.Message) -> bool:
#         user_data = get_employee(message.from_user.id)
#         if user_data.get('position') == 'admin' or message.from_user.id in ADMINS:
#             return True
#         else:
#             return False