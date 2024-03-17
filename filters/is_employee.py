from aiogram.filters import Filter
from aiogram import types
from api import get_employee

class IsEmployee(Filter):
    async def __call__(self, message: types.Message) -> bool:
        user_data = get_employee(message.from_user.id)
        if user_data.get('position') in ['worker', 'student']:
            return True
        else:
            return False