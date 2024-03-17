
import asyncio
import os
import logging
import sys
import sqlalchemy
import db_01


from aiogram import Bot, Dispatcher, F, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
import keyboards as kb
from dotenv import load_dotenv
from aiogram.client.bot import DefaultBotProperties
from connection import BD
from connection import cursor

tabl = BD()
resultSelect = tabl.ss()
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
    if db_01.user_exist(user_contact):
        if db_01.user_status(user_contact):
            await message.answer("Статус пользователя активен. Вам открыт доступ к заявкам. Добро пожаловать!", reply_markup=kb.function_keyboard())
            user_contact = str(contact.phone_number)
            key_admin = True
        else:
            await message.answer(f"Статус пользователя не активен. Вам закрыт доступ к заявкам")
    else:
        await message.answer(f"Данного номера нет в базе сотрудников.")


@dp.message(lambda message: key_admin == True and(F.text == 'Просмотр заявок' or
                                                  F.text == 'Редактировать заявку' or F.text == 'Подать заявку'))
async def view_report(message: types.Message):
    if message.text == 'Просмотр заявок':
        await message.answer(resultSelect)
    elif message.text == 'Редактировать заявку':
        await message.answer("Введите ID заявки:")
        request_id = message.text
        await message.answer("Что изменить:", reply_markup=kb.edit_keyboard())
    elif message.text == 'Подать заявку':
        await message.answer("Здесь будет реализована функция подача заявки.")

@dp.message(lambda message: key_admin == True and(F.text == 'Заявка' or
                                                  F.text == 'Статус заявки' or F.text == 'ID пользователя'
                                                  or F.text == 'Ответственный за исполнение' or F.text == 'Начало исполнения'
                                                  or F.text == 'Конец исполнения'))
async def work_report(message: types.Message):
    if message.text == 'Заявка':
        # appEdit = message.text
        # cursor.execute("UPDATE applicationss SET app ="+ str(appEdit)+ "WHERE id = 1 " )
        # appEditText =
        await message.answer("функция редактирования столбца 'заявка'.")
    if message.text == 'Статус заявки':
        await message.answer("функция редактирования столбца 'Статус заявки'.")
    if message.text == 'ID пользователя':
        await message.answer("функция редактирования столбца 'ID пользователя'.")
    if message.text == 'Ответственный за исполнение':
        await message.answer("функция редактирования столбца 'Ответственный за исполнение'.")
    if message.text == 'Начало исполнения':
        await message.answer("функция редактирования столбца 'Начало исполнения'.")
    if message.text == 'Конец исполнения':
        await message.answer("функция редактирования столбца 'Конец исполнения'.")



#@dp.message()
#async def process_id(message: types.Message):
    #request_id = message.text  # сделайте чтоб вызывалась строка по введенному id
    #await message.answer("Что изменить:", reply_markup=kb.edit_keyboard())


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())