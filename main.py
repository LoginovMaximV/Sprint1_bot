#Удачи
import asyncio, os
import logging
import sys

from aiogram import Bot, Dispatcher, F, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
#from aiogram.utils.markdown import hbold
from keyboards import contact_keyboard
from dotenv import load_dotenv
from aiogram.exceptions import AiogramError

load_dotenv()
TOKEN = os.getenv('TOKEN')
bot = Bot(TOKEN)
dp = Dispatcher()
admin_phone_number = os.getenv("ADMIN_NUMBER")
@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(text="Здравствуйте!\n"
                              "Отправьте номер телефона для авторизации.", reply_markup=contact_keyboard())

@dp.message(F.contact)
async def get_contact(message: types.Message):
    contact = message.contact
    if contact.phone_number == admin_phone_number:
        await message.answer("Добро пожаловать!")
        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
        except AiogramError:
            pass
    else:
        await message.answer("Данного номера нет в базе сотрудников.")


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())