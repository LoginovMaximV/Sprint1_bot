import asyncio
import os
import logging
import sys
import db_01

from aiogram import Bot, Dispatcher, F, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
import keyboards as kb
from dotenv import load_dotenv
from aiogram.client.bot import DefaultBotProperties

load_dotenv()
TOKEN = os.getenv('TOKEN')
bot = Bot(TOKEN)
dp = Dispatcher()
admin_phone_number = os.getenv("ADMIN_NUMBER")
user_contact = ''
key_admin = False

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(text="Здравствуйте!\n"
                              "Отправьте номер телефона для авторизации.", reply_markup=kb.contact_keyboard())

@dp.message(F.contact)
async def get_contact(message: types.Message):
    contact = message.contact
    global user_contact
    global key_admin
    user_contact = str(contact.phone_number)
    if user_contact[:1] == '+':
        user_contact = user_contact[1:]
    #if db_01.user_exist(user_contact):
    if user_contact == admin_phone_number:
        await message.answer("Добро пожаловать!", reply_markup=kb.function_keyboard())
        user_contact = str(contact.phone_number)
        key_admin = True
    else:
        await message.answer(f"Данного номера нет в базе сотрудников.")


#@dp.message(lambda message: key_admin == True and F.text == 'Подать заявку')
#async def new_report(message: types.Message):
    #await message.answer("Здесь будет реализована функция подача заявки.")


@dp.message(lambda message: key_admin == True and F.text == 'Просмотр заявок')
async def view_report(message: types.Message):
    if message.text == 'Просмотр заявок':
        await message.answer("Здесь будет реализована функция просмотра заявок.")
    elif message.text == 'Редактировать заявку':
        await message.answer("Введите ID заявки:")
        request_id = message.text
        await message.answer("Что изменить:", reply_markup=kb.edit_keyboard())
    elif message.text == 'Подать заявку':
        await message.answer("Здесь будет реализована функция подача заявки.")


#@dp.message(lambda message: key_admin == True and F.text == 'Редактировать заявку')
#async def edit_report(message: types.Message):
    #await message.answer("Введите ID заявки:")


@dp.message()
async def process_id(message: types.Message):
    request_id = message.text  # сделайте чтоб вызывалась строка по введенному id
    await message.answer("Что изменить:", reply_markup=kb.edit_keyboard())


@dp.message(lambda message: key_admin == True and F.text == 'Заявка')
async def new_report(message: types.Message):
    await message.answer("функция редактирования столбца 'заявка'.")


@dp.message(lambda message: key_admin == True and F.text == 'Статус заявки')
async def new_report(message: types.Message):
    await message.answer("функция редактирования столбца 'Статус заявки'.")


@dp.message(lambda message: key_admin == True and F.text == 'ID пользователя')
async def new_report(message: types.Message):
    await message.answer("функция редактирования столбца 'ID пользователя'.")


@dp.message(lambda message: key_admin == True and F.text == 'Ответственный за исполнение')
async def new_report(message: types.Message):
    await message.answer("функция редактирования столбца 'Ответственный за исполнение'.")


@dp.message(lambda message: key_admin == True and F.text == 'Начало исполнения')
async def new_report(message: types.Message):
    await message.answer("функция редактирования столбца 'Начало исполнения'.")


@dp.message(lambda message: key_admin == True and F.text == 'Конец исполнения')
async def new_report(message: types.Message):
    await message.answer("функция редактирования столбца 'Конец исполнения'.")


async def main() -> None:
    bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())