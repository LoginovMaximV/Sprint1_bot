import db_01

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

#Нужно протестировать!
#"email_id": "{report_data['email_name']}"
#@auth
#@dp.message(HelpDesk.choosing_os)
#async def report_chosen(message: Message, state: FSMContext):
    #await state.update_data(email_name=message.text)
    #await message.answer(
      #  text="Введите свой email:")
    #await state.set_state(HelpDesk.writing_email)