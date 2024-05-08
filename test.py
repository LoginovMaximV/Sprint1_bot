import db_01
import requests

from db_01 import User, session, user_exist, user_status

user_contact = ''


def auth(func):
    def wrapper(*args, **kwargs):
        if db_01.user_exist(user_contact):
            return func(*args, **kwargs)
        else:
            return 'Доступ заблокирован'
    return wrapper


