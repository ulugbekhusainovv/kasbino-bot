import handlers,middlewares
from loader import dp,bot
from aiogram.types.bot_command_scope_all_private_chats import BotCommandScopeAllPrivateChats
import asyncio
from utils.notify_admins import start,shutdown
from utils.set_botcommands import commands
from api import set_all_employee_change_status
from datetime import datetime,  timedelta
import threading
import logging
import sys, pytz, schedule, time


async def main():
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await bot.set_my_commands(commands=commands,scope=BotCommandScopeAllPrivateChats(type='all_private_chats'))
        dp.startup.register(start)
        dp.shutdown.register(shutdown)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

async def note_schedule():
    set_all_employee_change_status()

def schedule_thread():
    schedule.every().day.at("23:59",'Asia/Tashkent').do(asyncio.run, note_schedule())

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    threading.Thread(target=schedule_thread, daemon=True).start()
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())





