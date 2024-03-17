from loader import dp
from aiogram import types,F
from api import get_user, create_user
import re


def html_escape(text):
    escape_chars = {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}
    return re.sub(r'[&<>"\']', lambda match: escape_chars[match.group(0)], text)



@dp.message(F.text)
async def echo_bot(message:types.Message):
    user = get_user(telegram_id=message.from_user.id)
    full_name =  html_escape(message.from_user.full_name)
    if not user:
        user = create_user(telegram_id=message.from_user.id, full_name=full_name)
    await message.answer(message.text)
