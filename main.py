import asyncio
import json
import os
import logging
import sys
import db_01
import requests
import aiohttp


from aiogram import Bot, Dispatcher, F, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
import keyboards as kb
from dotenv import load_dotenv
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from db_01 import User, session, Category, Problem
from test import auth
from aiogram.types import FSInputFile


base_url = 'https://141.101.201.70:8444/api/v3'
headers = {"authtoken": "E84D46D9-112E-4B39-BC6D-464AB2711C29"}
load_dotenv()
TOKEN = os.getenv('TOKEN')
bot = Bot(TOKEN)
dp = Dispatcher()
admin_phone_number = os.getenv("ADMIN_NUMBER")
user_contact = ''
matched_user = ''
probl = []
key_av = False
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
    admin_search = State()


@dp.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await message.answer(text="Привет!\n"
                              "Я - бот HelpDesk, сделанный для упрощения работы с заявками.\n"
                              "Вы можете просматривать и подавать заявки.\n"
                              "Для начала работы необходимо авторизоваться по номеру телефона. \n"
                              "Просто нажмите кнопку 'Отправить'.", reply_markup=kb.contact_keyboard())
    await state.set_state(HelpDesk.getting_name)


@dp.message(HelpDesk.getting_name, F.contact)
async def get_contact(message: types.Message, state: FSMContext):
    contact = message.contact
    global user_contact
    global key_av
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
                await message.answer("Статус пользователя активен. \n"
                                     "Вам открыт доступ к заявкам. \n"
                                     "Добро пожаловать " + matched_user.name + '!',
                                     reply_markup=kb.function_keyboard())
                user_contact = str(contact.phone_number)
                key_av = True
                key_admin = db_01.User.get_admin_status(user_contact)
                await state.update_data(user_name=matched_user.name)
            else:
                await message.answer("Соответствующий пользователь не найден.")
        else:
            await message.answer(f"Статус пользователя не активен. Вам закрыт доступ к заявкам")
    else:
        await message.answer(f"Данного номера нет в базе сотрудников.")


@auth
@dp.message(lambda message: key_admin == True, F.text == 'Просмотр заявок')
async def search_request(message: types.Message,state: FSMContext):
    await message.answer("Введите номер заявки:")

    await state.set_state(HelpDesk.admin_search)


@auth
@dp.message(lambda message: key_admin == True, HelpDesk.admin_search)
async def view_report(message: types.Message):
    request_number = message.text

    url = f"{base_url}/requests"
    input_data = f'''{{
            "list_info": {{
                "row_count": 100,
                "start_index": 1,
                "sort_field": "subject",
                "sort_order": "asc",
                "get_total_count": true,
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
                if request_number == request['id']:
                    request_id = request['id']
                    subject = request['subject']
                    description = request['short_description']
                    name = request['requester']['name']
                    status = request['status']['name']
                    group = request['group']['name']
                    finish_time = request['due_by_time']['display_value']
                    await message.answer(
                        f"ID:{request_id} {subject}\n"
                        f"Имя: {name}\n"
                        f"Описание: {description}\n"
                        f"Статус: {status}\n"
                        f"Группа: {group}\n"
                        f"Срок выполнения: {finish_time}"
                    )



        else:
            await message.answer(f"Не найдено заявок ")
    else:
        await message.answer("Ошибка при получении данных. Попробуйте позже.")


@auth
@dp.message(lambda message: key_av == True, F.text == 'Просмотр заявок')
async def view_report(message: types.Message):
    url = f"{base_url}/requests"
    input_data = f'''{{
        "list_info": {{
            "row_count": 20,
            "start_index": 1,
            "sort_field": "subject",
            "sort_order": "asc",
            "get_total_count": true,
            "search_fields": {{
                "requester.name": "test.test",
            }},
        }}
    }}'''
    # в "requester.name": "{matched_user.name}"
    params = {'input_data': input_data}
    response = requests.get(url, headers=headers, params=params, verify=False)
    print(response.text)
    if response.status_code == 200:
        data = response.json()
        requests_list = data.get('requests', [])

        if requests_list:
            for request in requests_list:
                request_id = request['id']
                subject = request['subject']
                description = request['short_description'][:150]
                status = request['status']['name']
                group = request['group']['name']
                finish_time = request['due_by_time']['display_value']
                await message.answer(
                                     f"ID:{request_id} {subject}\n"
                                     f"Имя: {matched_user.name}\n"
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
@dp.message(lambda message: key_av == True, F.text == 'Подать заявку')
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
        caption=f"Вы ввели следующие данные: \n"
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


async def send_to_helpdesk(subject: str, user_name: str, description: str, email: str, phone_number: str,  vip: str, category_id:str,name_problem:str,problem_id:str):
    url = f"{base_url}/requests"
    input_data = json.dumps({
        "request": {
            "subject": subject,
            "description": description,
            "requester": {
                "email_id": email,
                "phone": phone_number,
                "name": user_name,
                "is_vipuser": vip,
            },
            "template": {
                "is_service_template": True,
                "service_category": {
                    "id": category_id
                    },
                "name": name_problem,
                "id": problem_id
                },
            }
    })

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data={'input_data': input_data}, ssl=False) as response:
            response_text = await response.text()
            print(response_text)
            return json.loads(response_text)


@auth
@dp.message(HelpDesk.send_or_cancel, F.text == 'Отправить')
async def send(message: Message, state: FSMContext):
    report_data = await state.get_data()
    matched_user.email = str(matched_user.email)
    matched_user.number = str(matched_user.number)
    matched_user.vip = matched_user.vip
    category_id = str(Category.get_id_by_name(report_data['chosen_problem_category']))
    problem_id = str(Problem.get_id_by_name(report_data['chosen_problem']))
    response_json = await send_to_helpdesk(report_data['chosen_problem'], matched_user.name,
                                           f"{report_data['theme']}: {report_data['user_description']}",
                                           matched_user.email, matched_user.number, matched_user.vip, category_id, problem_id, report_data['chosen_problem']
                                           )
    print(response_json)
    request_id = response_json["request"]["id"]

    fileg = report_data['user_screenshot']
    file_info = await bot.get_file(fileg)
    file_path = file_info.file_path
    file_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"
    print(file_url)

    def add_attach_file(url: str, endpoint: str, request_id: int, file_url: str) -> int:
        url1 = f"{url}/{endpoint}/{request_id}/upload"
        response = requests.get(file_url, stream=True)
        files = {'file': (file_url.split("/")[-1], response.raw, 'image/jpeg')}
        responsed = requests.put(url1, headers=headers, files=files, verify=False)
        return responsed.status_code

    s = add_attach_file(base_url, "requests", request_id, file_url)
    print(s)
    await message.answer(f"Заявка успешно подана!\nНомер вашей заявки {request_id}")
    await state.clear()


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
