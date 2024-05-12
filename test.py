import db_01
import requests

from db_01 import User, session, user_exist, user_status

user_contact = ''


def auth(func):
    def wrapper(*args, **kwargs):
        if db_01.user_exist(user_contact):
            if db_01.user_status(user_contact):
                return func(*args, **kwargs)
            else:
                return 'Доступ заблокирован'
    return wrapper


###все, что связано с редактированием заявки###

# @auth
# @dp.message(lambda message: key_admin == True, F.text == 'Просмотр заявок', HelpDesk.choosing_report_number)
# async def view_report(message: types.Message):
#     await message.answer(resultSelect)
#     await message.answer('Введите номер редактируемой заявки:')
#
# @auth
# @dp.message(lambda message: F.text == 'Редактировать заявку')
# async def edit_report(message: types.Message, state: FSMContext):
#     await state.set_state(HelpDesk.choosing_report_number)
#     await message.answer("Просмотрите заявки и введите номер редактируемой заявки:", reply_markup=kb.view_keyboard())
#
#
# @auth
# @dp.message(HelpDesk.choosing_report_number)
# async def report_number(message: types.Message, state: FSMContext):
#     await state.update_data(number_report=message.text)
#     data = await state.get_data()
#     await message.answer(f'Выберите, что необходимо изменить. \n report_number: {data['number_report']}',  #здесь проверил сохранение введенного номера
#                          reply_markup=kb.edit_keyboard())
#     await state.clear()
#
#
#
# @auth
# @dp.message(lambda message: F.text == 'Заявка')
# async def work_report(message: types.Message):
#     # appEdit = message.text
#     # cursor.execute("UPDATE applicationss SET app ="+ str(appEdit)+ "WHERE id = 1 " )
#     # appEditText =
#     await message.answer("функция редактирования столбца 'заявка'.")
#
#
# @auth
# @dp.message(lambda message: F.text == 'Статус заявки')
# async def work_status(message: types.Message):
#     await message.answer("функция редактирования столбца 'Статус заявки'.")
#
#
# @auth
# @dp.message(lambda message: F.text == 'ID пользователя')
# async def work_id(message: types.Message):
#     await message.answer("функция редактирования столбца 'ID пользователя'.")
#
#
# @auth
# @dp.message(lambda message: F.text == 'Ответственный за исполнение')
# async def work_employer(message: types.Message):
#     await message.answer("функция редактирования столбца 'Ответственный за исполнение'.")
#
#
# @auth
# @dp.message(lambda message: F.text == 'Начало исполнения')
# async def work_start(message: types.Message):
#     await message.answer("функция редактирования столбца 'Начало исполнения'.")
#
#
# @auth
# @dp.message(lambda message: F.text == 'Конец исполнения')
# async def work_finish(message: types.Message):
#     await message.answer("функция редактирования столбца 'Конец исполнения'.")
#
#

