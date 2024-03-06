from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def authorization_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Войти")
    kb.adjust()
    return kb.as_markup(resize_keyboard=True)

def contact_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Отправить", request_contact=True)
    kb.adjust()
    return kb.as_markup(resize_keyboard=True)