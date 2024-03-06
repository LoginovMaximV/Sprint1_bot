from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def contact_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Отправить", request_contact=True)
    kb.adjust()
    return kb.as_markup(resize_keyboard=True)
def function_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Подать заявку")
    kb.button(text="Просмотр заявок")
    kb.button(text="Редактировать заявку")
    kb.adjust()
    return kb.as_markup(resize_keyboard=True)