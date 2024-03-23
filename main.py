
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
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

tabl = BD()
resultSelect = tabl.ss()
load_dotenv()
TOKEN = os.getenv('TOKEN')
bot = Bot(TOKEN)
dp = Dispatcher()
admin_phone_number = os.getenv("ADMIN_NUMBER")
user_contact = ''
key_admin = False
available_problem_types = ["Проблема с интернетом"]
available_os_types = ["Windows", "macOS", "Linux"]
available_answers = ["Отправить", "Отменить"]


class HelpDesk(StatesGroup):
    choosing_report_number = State()
    choosing_problem_type = State()
    choosing_os = State()
    writing_address = State()
    writing_network_name = State()
    send_or_cancel = State()
    uncommon_problem = State()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(text="Привет!\n"
                              "Я - бот HelpDesk, сделанный для упрощения работы с заявками. "
                              "Вы можете просматривать, редактировать и подавать заявки. Для начала "
                              "работы необходимо авторизоваться по номеру телефона — просто нажмите "
                              "кнопку 'Отправить'.", reply_markup=kb.contact_keyboard())


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
            await message.answer("Статус пользователя активен. Вам открыт доступ к заявкам. Добро пожаловать!",
                                 reply_markup=kb.function_keyboard())
            user_contact = str(contact.phone_number)
            key_admin = True
        else:
            await message.answer(f"Статус пользователя не активен. Вам закрыт доступ к заявкам")
    else:
        await message.answer(f"Данного номера нет в базе сотрудников.")


@dp.message(lambda message: key_admin == True, F.text == 'Просмотр заявок', HelpDesk.choosing_report_number)
async def view_report(message: types.Message):
    await message.answer(resultSelect)
    await message.answer('Введите номер редактируемой заявки:')


@dp.message(lambda message: key_admin == True, F.text == 'Просмотр заявок')
async def view_report(message: types.Message):
    await message.answer(resultSelect)


@dp.message(lambda message: key_admin == True, F.text == 'Редактировать заявку')
async def edit_report(message: types.Message, state: FSMContext):
    await state.set_state(HelpDesk.choosing_report_number)
    await message.answer("Просмотрите заявки и введите номер редактируемой заявки:", reply_markup=kb.view_keyboard())


@dp.message(HelpDesk.choosing_report_number)
async def report_number(message: types.Message, state: FSMContext):
    await state.update_data(number_report=message.text)
    data = await state.get_data() #здесь хранится номер заявки
    await message.answer(f'Выберите, что необходимо изменить. \n report_number: {data['number_report']}',  #здесь проверил сохранение введенного номера
                         reply_markup=kb.edit_keyboard())
    await state.clear()


@dp.message(lambda message:key_admin == True, F.text == 'Подать заявку')
async def new_report(message: types.Message, state: FSMContext):
    await message.answer("Выберите проблему из списка:", reply_markup=kb.report_keyboard())
    await state.set_state(HelpDesk.choosing_problem_type)


@dp.message(HelpDesk.choosing_problem_type, F.text == 'Другое')
async def report_chosen(message: Message, state: FSMContext):
    await message.answer(
        text="Кратко опишите вашу проблему:")
    await state.set_state(HelpDesk.uncommon_problem)


@dp.message(HelpDesk.choosing_problem_type, F.text.in_(available_problem_types))
async def report_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_problem=message.text)
    await message.answer(
        text="Введите название вашей сети:")
    await state.set_state(HelpDesk.writing_network_name)


@dp.message(HelpDesk.uncommon_problem)
async def report_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_problem=message.text)
    await message.answer(
        text="Введите название вашей сети:")
    await state.set_state(HelpDesk.writing_network_name)


@dp.message(HelpDesk.writing_network_name)
async def report_chosen(message: Message, state: FSMContext):
    await state.update_data(network_name=message.text)
    await message.answer(
        text="Укажите вашу ОС:",
        reply_markup=kb.os_choose()
    )
    await state.set_state(HelpDesk.choosing_os)


@dp.message(HelpDesk.choosing_os, F.text.in_(available_os_types))
async def report_chosen(message: Message, state: FSMContext):
    await state.update_data(chosen_os=message.text)
    await message.answer(
        text="Введите ваш адрес:")
    await state.set_state(HelpDesk.writing_address)


@dp.message(HelpDesk.writing_address)
async def report_chosen(message: Message, state: FSMContext):
    await state.update_data(user_address=message.text)
    report_data = await state.get_data()
    await message.answer(
        text=f"Вы ввели следующие данные: \nПроблема: {report_data['chosen_problem']} \n"
             f"Название сети: {report_data['network_name']} \n"
             f"Операционная система: {report_data['chosen_os']} \n"
             f"Адрес: {report_data['user_address']} \n"
             f"Если все верно, то нажмите кнопку 'Отправить'. Иначе - кнопку 'Отменить'.", reply_markup=kb.new_report_keyboard())
    await state.set_state(HelpDesk.send_or_cancel)


@dp.message(HelpDesk.send_or_cancel, F.text == 'Отменить')
async def cancel(message: Message, state: FSMContext):
    await message.answer(text="Подача заявки отменена.", reply_markup=kb.function_keyboard())
    await state.clear()


@dp.message(HelpDesk.send_or_cancel, F.text == 'Отправить')
async def send(message: Message, state: FSMContext):
    # здесь уже сами реализуете функцию подачи
    await message.answer(text="Заявка успешно подана!", reply_markup=kb.function_keyboard())
    await state.clear()


@dp.message(lambda message: key_admin == True, F.text == 'Заявка')
async def work_report(message: types.Message):
    # appEdit = message.text
    # cursor.execute("UPDATE applicationss SET app ="+ str(appEdit)+ "WHERE id = 1 " )
    # appEditText =
    await message.answer("функция редактирования столбца 'заявка'.")


@dp.message(lambda message: key_admin == True, F.text == 'Статус заявки')
async def work_status(message: types.Message):
    await message.answer("функция редактирования столбца 'Статус заявки'.")


@dp.message(lambda message: key_admin == True, F.text == 'ID пользователя')
async def work_id(message: types.Message):
    await message.answer("функция редактирования столбца 'ID пользователя'.")


@dp.message(lambda message: key_admin == True, F.text == 'Ответственный за исполнение')
async def work_employer(message: types.Message):
    await message.answer("функция редактирования столбца 'Ответственный за исполнение'.")


@dp.message(lambda message: key_admin == True, F.text == 'Начало исполнения')
async def work_start(message: types.Message):
    await message.answer("функция редактирования столбца 'Начало исполнения'.")


@dp.message(lambda message: key_admin == True, F.text == 'Конец исполнения')
async def work_finish(message: types.Message):
    await message.answer("функция редактирования столбца 'Конец исполнения'.")


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())