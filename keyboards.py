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


def edit_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Заявка")
    kb.button(text="Статус заявки")
    kb.button(text="ID пользователя")
    kb.button(text="Ответственный за исполнение")
    kb.button(text="Начало исполнения")
    kb.button(text="Конец исполнения")
    kb.adjust(1, 1)
    return kb.as_markup(resize_keyboard=True)


def view_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Просмотр заявок")
    kb.adjust()
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=True)

