import asyncio
import json
import os
import logging
import sys
import db_01
import requests


from aiogram import Bot, Dispatcher, F, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
import keyboards as kb
from dotenv import load_dotenv
from connection import BD
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from db_01 import User, session
from test import auth
from aiogram.types import FSInputFile


url = 'https://141.101.201.70:8444/api/v3/requests'
headers = {"authtoken": "4BE102E2-449D-4D37-8BC7-167BEF0ACCC7"}
tabl = BD()
resultSelect = tabl.ss()
load_dotenv()
TOKEN = os.getenv('TOKEN')
bot = Bot(TOKEN)
dp = Dispatcher()
admin_phone_number = os.getenv("ADMIN_NUMBER")
user_contact = ''
matched_user = ''
probl = []
key_admin = False
available_problem_categories = db_01.Category.get_all_name()
available_os_types = ["Windows", "macOS", "Linux"]
available_answers = ["Отправить", "Отменить"]


class HelpDesk(StatesGroup):
    getting_name = State()
    choosing_report_number = State()
    choosing_problem_category = State()
    choosing_problem_type = State()
    description = State()
    writing_theme = State()
    send_or_cancel = State()
    uncommon_problem = State()
    sending_screenshot = State()


@dp.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await message.answer(text="Привет!\n"
                              "Я - бот HelpDesk, сделанный для упрощения работы с заявками.\n"
                              "Вы можете просматривать, редактировать и подавать заявки.\n"
                              "Для начала работы необходимо авторизоваться по номеру телефона \n"
                              " — просто нажмите кнопку 'Отправить'.", reply_markup=kb.contact_keyboard())
    await state.set_state(HelpDesk.getting_name)


@dp.message(HelpDesk.getting_name, F.contact)
async def get_contact(message: types.Message, state: FSMContext):
    contact = message.contact
    global user_contact
    global key_admin
    global matched_user
    user_contact = str(contact.phone_number)
    if user_contact.startswith('7'):
        user_contact = '+' + user_contact

    if db_01.user_exist(user_contact):
        if db_01.user_status(user_contact):
            matched_user = session.query(User).filter(User.number == str(user_contact)).first()
            matched_user.name = str(matched_user.name)
            if matched_user:
                await message.answer("Статус пользователя активен. Вам открыт доступ к заявкам. "
                                     "Добро пожаловать " + matched_user.name + '!',
                                     reply_markup=kb.function_keyboard())
                user_contact = str(contact.phone_number)
                key_admin = True
                await state.update_data(user_name=matched_user.name)
            else:
                await message.answer("Соответствующий пользователь не найден.")
        else:
            await message.answer(f"Статус пользователя не активен. Вам закрыт доступ к заявкам")
    else:
        await message.answer(f"Данного номера нет в базе сотрудников.")


@auth
@dp.message(lambda message: key_admin == True, F.text == 'Просмотр заявок', HelpDesk.choosing_report_number)
async def view_report(message: types.Message):
    await message.answer(resultSelect)
    await message.answer('Введите номер редактируемой заявки:')


@auth
@dp.message(lambda message: key_admin == True, F.text == 'Просмотр заявок')
async def view_report(message: types.Message):
    input_data = f'''{{
        "list_info": {{
            "row_count": 20,
            "start_index": 1,
            "sort_field": "subject",
            "sort_order": "asc",
            "get_total_count": true,
            "search_fields": {{
                "requester.name": "Баканов Артур Андреевич",
            }},
        }}
    }}'''
    params = {'input_data': input_data}
    response = requests.get(url, headers=headers, params=params, verify=False)
    print(response.text)
    if response.status_code == 200:
        data = response.json()
        requests_list = data.get('requests', [])

        if requests_list:
            for request in requests_list:
                #request_id = request['request']['id']
                subject = request['subject']
                description = request['short_description']
                status = request['status']['name']
                group = request['group']['name']
                finish_time = request['due_by_time']['display_value']
                await message.answer(
                                     f" {subject}\n"
                                     f"Описание: {description}\n"
                                     f"Статус: {status}\n"
                                     f"Группа: {group}\n"
                                     f"Срок выполнения: {finish_time}"
                )
        else:
            await message.answer(f"Не найдено заявок для пользователя {matched_user.name}")
    else:
        await message.answer("Ошибка при получении данных. Попробуйте позже.")


@auth
@dp.message(lambda message: key_admin == True, F.text == 'Подать заявку')
async def new_report(message: types.Message, state: FSMContext):
    await message.answer("Выберите категорию:", reply_markup=kb.problem_category())
    await state.set_state(HelpDesk.choosing_problem_category)


@auth
@dp.message(HelpDesk.choosing_problem_category, F.text.in_(available_problem_categories))
async def report_chosen(message: Message, state: FSMContext):
    cat_name = message.text
    cat_id = db_01.Category.get_id_by_name(cat_name)
    global probl
    probl = db_01.Problem.get_names_by_id(cat_id)
    for x in probl:
        kb = [
            [
                types.KeyboardButton(text=x)
            ],
        ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await state.update_data(chosen_problem_category=message.text)
    await message.answer(
        text="Выберите услугу:",
        reply_markup=keyboard)
    await state.set_state(HelpDesk.choosing_problem_type)


@auth
@dp.message(HelpDesk.choosing_problem_category, F.text == 'Другое')
async def theme(message: Message, state: FSMContext):
    await state.update_data(chosen_problem=message.text, chosen_problem_category='Другое')
    await message.answer(
        text="Тема обращения:")
    await state.set_state(HelpDesk.writing_theme)


@auth
@dp.message(HelpDesk.choosing_problem_type)
async def theme(message: Message, state: FSMContext):
    await state.update_data(chosen_problem=message.text)
    await message.answer(
        text="Тема обращения:")
    await state.set_state(HelpDesk.writing_theme)


@auth
@dp.message(HelpDesk.writing_theme)
async def description(message: Message, state: FSMContext):
    await state.update_data(theme=message.text)
    await message.answer(
        text="Опишите проблему:")
    await state.set_state(HelpDesk.description)


@auth
@dp.message(HelpDesk.description)
async def screenshot1(message: Message, state: FSMContext):
    await state.update_data(user_description=message.text)
    await message.answer(
        text="Приложите скриншот:",
        reply_markup=kb.screenshot())
    await state.set_state(HelpDesk.sending_screenshot)


@auth
@dp.message(HelpDesk.sending_screenshot, F.text == 'Отменить')
async def screenshot(message: Message, state: FSMContext):
    photod = FSInputFile("no_screen.png")
    await state.update_data(user_screenshot=photod)
    report_data = await state.get_data()
    await message.answer_photo(
        report_data['user_screenshot'],
        caption=f"Вы ввели следующие данные:  \nЗаявитель: {report_data['user_name']} \n"
                f"Категория: {report_data['chosen_problem_category']} \n"
                f"Услуга: {report_data['chosen_problem']} \n"
                f"Тема: {report_data['theme']} \n"
                f"Описание: {report_data['user_description']} \n"
                f"Если все верно, то нажмите кнопку 'Отправить'. Иначе - кнопку 'Отменить'.",
        reply_markup=kb.new_report_keyboard())
    await state.set_state(HelpDesk.send_or_cancel)


@auth
@dp.message(HelpDesk.sending_screenshot, F.photo)
async def screenshot(message: Message, state: FSMContext):
    await state.update_data(user_screenshot=message.photo[-1].file_id)
    report_data = await state.get_data()
    await message.answer_photo(
        report_data['user_screenshot'],
        caption=f"Вы ввели следующие данные: \nЗаявитель: {report_data['user_name']} \n"
                f"Категория: {report_data['chosen_problem_category']} \n"
                f"Услуга: {report_data['chosen_problem']} \n"
                f"Тема: {report_data['theme']} \n"
                f"Описание: {report_data['user_description']} \n"
                f"Если все верно, то нажмите кнопку 'Отправить'. Иначе - кнопку 'Отменить'.",
        reply_markup=kb.new_report_keyboard())
    await state.set_state(HelpDesk.send_or_cancel)


@auth
@dp.message(HelpDesk.send_or_cancel, F.text == 'Отменить')
async def cancel(message: Message, state: FSMContext):
    await message.answer(text="Подача заявки отменена.", reply_markup=kb.function_keyboard())
    await state.clear()


@auth
@dp.message(HelpDesk.send_or_cancel, F.text == 'Отправить')
async def send(message: Message, state: FSMContext):
    report_data = await state.get_data()
    input_data = f'''{{
        "request": {{
            "subject": "{report_data['chosen_problem']}",
            "description": "{report_data['theme']}: {report_data['user_description']}",
            "requester": {{
                "id": "4",
                "name": "{report_data['user_name']}",
            }}
        }}
    }}'''
    data = {'input_data': str(input_data)}
    response = requests.post(url, headers=headers, data=data, verify=False)
    print(response.text)
    json_data = json.loads(response.text)
    print(json_data)
    request_id = json_data["request"]["id"]
    await message.answer(text="Заявка успешно подана!\n"
                              f"Номер вашей заявки {request_id}", reply_markup=kb.function_keyboard())

    await state.clear()


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
