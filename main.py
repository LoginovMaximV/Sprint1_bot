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
key_admin = False
available_problem_types = db_01.Buttons.get_all_problems()
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
    writing_email = State()
    sending_screenshot = State()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(text="Привет!\n"
                              "Я - бот HelpDesk, сделанный для упрощения работы с заявками.\n"
                              "Вы можете просматривать, редактировать и подавать заявки.\n"
                              "Для начала работы необходимо авторизоваться по номеру телефона \n"
                              " — просто нажмите кнопку 'Отправить'.", reply_markup=kb.contact_keyboard())


@dp.message(F.contact)
async def get_contact(message: types.Message):
    contact = message.contact
    global user_contact
    global key_admin
    user_contact = str(contact.phone_number)
    if user_contact.startswith('+'):
        user_contact = user_contact[1:]

    global matched_user
    matched_user = session.query(User).filter(User.number == int(user_contact)).first()
    matched_user.name = str(matched_user.name)

    if db_01.user_exist(user_contact):
        if db_01.user_status(user_contact):
            if matched_user:
                await message.answer("Статус пользователя активен. Вам открыт доступ к заявкам. "
                                     "Добро пожаловать " + matched_user.name + '!',
                                     reply_markup=kb.function_keyboard())
                user_contact = str(contact.phone_number)
                key_admin = True
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
@dp.message(lambda message: key_admin == True, F.text == 'Редактировать заявку')
async def edit_report(message: types.Message, state: FSMContext):
    await state.set_state(HelpDesk.choosing_report_number)
    await message.answer("Просмотрите заявки и введите номер редактируемой заявки:", reply_markup=kb.view_keyboard())


@auth
@dp.message(HelpDesk.choosing_report_number)
async def report_number(message: types.Message, state: FSMContext):
    await state.update_data(number_report=message.text)
    data = await state.get_data()
    await message.answer(f'Выберите, что необходимо изменить. \n report_number: {data['number_report']}',  #здесь проверил сохранение введенного номера
                         reply_markup=kb.edit_keyboard())
    await state.clear()


@auth
@dp.message(lambda message: key_admin == True, F.text == 'Подать заявку')
async def new_report(message: types.Message, state: FSMContext):
    await message.answer("Выберите проблему из списка:", reply_markup=kb.button_data())
    await state.set_state(HelpDesk.choosing_problem_type)


@auth
@dp.message(HelpDesk.choosing_problem_type, F.text == 'Другое')
async def report_chosen(message: Message, state: FSMContext):
    await message.answer(
        text="Кратко опишите вашу проблему:")
    await state.set_state(HelpDesk.uncommon_problem)


@auth
@dp.message(HelpDesk.choosing_problem_type, F.text.in_(available_problem_types))
async def wifi_name(message: Message, state: FSMContext):
    await state.update_data(chosen_problem=message.text)
    await message.answer(
        text="Введите название вашей сети:")
    await state.set_state(HelpDesk.writing_network_name)


@auth
@dp.message(HelpDesk.uncommon_problem)
async def wifi_name_uncommon(message: Message, state: FSMContext):
    await state.update_data(chosen_problem=message.text)
    await message.answer(
        text="Введите название вашей сети:")
    await state.set_state(HelpDesk.writing_network_name)


@auth
@dp.message(HelpDesk.writing_network_name)
async def os_type(message: Message, state: FSMContext):
    await state.update_data(network_name=message.text)
    await message.answer(
        text="Укажите вашу ОС:",
        reply_markup=kb.os_choose()
    )
    await state.set_state(HelpDesk.choosing_os)


@auth
@dp.message(HelpDesk.choosing_os, F.text.in_(available_os_types))
async def address(message: Message, state: FSMContext):
    await state.update_data(chosen_os=message.text)
    await message.answer(
        text="Введите ваш адрес:")
    await state.set_state(HelpDesk.writing_address)


@auth
@dp.message(HelpDesk.writing_address)
async def email_send(message: Message, state: FSMContext):
    await state.update_data(user_address=message.text)
    await message.answer(
        text="Приложите скриншот:",
        reply_markup=kb.screenshot())
    await state.set_state(HelpDesk.sending_screenshot)


@auth
@dp.message(HelpDesk.sending_screenshot, F.text == 'Отменить')
async def screenshot(message: Message, state: FSMContext):
    photod = FSInputFile("no_screen.png")
    await state.update_data(user_screenshot=photod)
    await message.answer(
        text="Введите свой email:")
    await state.set_state(HelpDesk.writing_email)




@auth
@dp.message(HelpDesk.sending_screenshot, F.photo)
async def screenshot(message: Message, state: FSMContext):
    await state.update_data(user_screenshot=message.photo[-1].file_id)
    await message.answer(
        text="Введите свой email:")
    await state.set_state(HelpDesk.writing_email)


@auth
@dp.message(HelpDesk.writing_email)
async def report_chosen(message: Message, state: FSMContext):
    await state.update_data(email_name=message.text)
    report_data = await state.get_data()
    await message.answer_photo(
        report_data['user_screenshot'],
        caption=f"Вы ввели следующие данные: \nПроблема: {report_data['chosen_problem']} \n"
             f"Название сети: {report_data['network_name']} \n"
             f"Операционная система: {report_data['chosen_os']} \n"
             f"Адрес: {report_data['user_address']} \n"
             f"Email: {report_data['email_name']} \n"
             f"Если все верно, то нажмите кнопку 'Отправить'. Иначе - кнопку 'Отменить'.", reply_markup=kb.new_report_keyboard())
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
            "description": "{report_data['network_name']}, {report_data['chosen_os']}, {report_data['user_address']}",
            "requester": {{
                "id": "4",
                "name": "{matched_user.name}",
            }}
        }}
    }}'''
    data = {'input_data': input_data}
    response = requests.post(url, headers=headers, data=data, verify=False)
    print(response.text)
    json_data = json.loads(response.text)
    print(json_data)
    request_id = json_data["request"]["id"]
    await message.answer(text="Заявка успешно подана!\n"
                              f"Номер вашей заявки {request_id}", reply_markup=kb.function_keyboard())

    await state.clear()


@auth
@dp.message(lambda message: key_admin == True, F.text == 'Заявка')
async def work_report(message: types.Message):
    # appEdit = message.text
    # cursor.execute("UPDATE applicationss SET app ="+ str(appEdit)+ "WHERE id = 1 " )
    # appEditText =
    await message.answer("функция редактирования столбца 'заявка'.")


@auth
@dp.message(lambda message: key_admin == True, F.text == 'Статус заявки')
async def work_status(message: types.Message):
    await message.answer("функция редактирования столбца 'Статус заявки'.")


@auth
@dp.message(lambda message: key_admin == True, F.text == 'ID пользователя')
async def work_id(message: types.Message):
    await message.answer("функция редактирования столбца 'ID пользователя'.")


@auth
@dp.message(lambda message: key_admin == True, F.text == 'Ответственный за исполнение')
async def work_employer(message: types.Message):
    await message.answer("функция редактирования столбца 'Ответственный за исполнение'.")


@auth
@dp.message(lambda message: key_admin == True, F.text == 'Начало исполнения')
async def work_start(message: types.Message):
    await message.answer("функция редактирования столбца 'Начало исполнения'.")


@auth
@dp.message(lambda message: key_admin == True, F.text == 'Конец исполнения')
async def work_finish(message: types.Message):
    await message.answer("функция редактирования столбца 'Конец исполнения'.")



async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
