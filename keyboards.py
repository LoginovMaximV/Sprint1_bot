from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import types
import db_01
import main


def contact_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Отправить", request_contact=True)
    kb.adjust()
    return kb.as_markup(resize_keyboard=True)


def function_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Подать заявку")
    kb.button(text="Просмотр заявок")
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


def report_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Проблема с интернетом")
    kb.button(text="Другое")
    kb.adjust(1, 1)
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=True)


def problem_category() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    problems = db_01.Category.get_all_name()

    for prob in problems:
        kb.button(text=prob)
    kb.adjust(5, 5)
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=True)


def problem_type() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    problems = main.probl
    for prob in problems:
        kb.button(text=prob)
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=True)


def os_choose() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="macOS")
    kb.button(text="Windows")
    kb.button(text="Linux")
    kb.adjust()
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=True)


def screenshot() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Отменить")
    kb.adjust()
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=True)


def new_report_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Отправить")
    kb.button(text="Отменить")
    kb.adjust(1,1)
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=True)
