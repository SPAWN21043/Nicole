from aiogram import types
from aiogram.types import ReplyKeyboardMarkup
from data_base.sql_db import read_salon
import sqlite3 as sq

base = sq.connect('nicole.db')
cur = base.cursor()


kb_start = ReplyKeyboardMarkup(resize_keyboard=True)
buttons = ['/start']
kb_start.add(*buttons)


kb_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
buttons = ['Услуги', 'Специалисты']
kb_keyboard.add(*buttons)
buttons2 = ['Информация о салонах']
kb_keyboard.add(*buttons2)
buttons3 = ['Помощь', 'ЛК']
kb_keyboard.add(*buttons3)


lk_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
buttons = ['Услуги', 'Специалисты']
lk_keyboard.add(*buttons)
buttons2 = ['Информация о салонах']
lk_keyboard.add(*buttons2)


def service_salon(m):
    ret = read_salon()
    buttons1 = []

    for item in ret:
        key_help = ["text", "callback_data"]
        record = dict.fromkeys(key_help, item[0])
        record.update({'callback_data': 'ID|'+str(item[1])})
        buttons1.append(record)

    ikw_kb = types.InlineKeyboardMarkup(row_width=2)
    ikw_kb.add(*buttons1)
    return ikw_kb


def master_salon(m):
    mast = read_salon()
    buttons1 = []

    for item in mast:
        key_help = ["text", "callback_data"]
        record = dict.fromkeys(key_help, item[0])
        record.update({'callback_data': 'M_ID|'+str(item[1])})
        buttons1.append(record)

    ikw_kb = types.InlineKeyboardMarkup(row_width=2)
    ikw_kb.add(*buttons1)
    return ikw_kb


def info_salon_info(m):
    inf = read_salon()
    buttons1 = []

    for item in inf:
        key_help = ["text", "callback_data"]
        record = dict.fromkeys(key_help, item[0])
        record.update({'callback_data': 'ISw|'+str(item[1])})
        buttons1.append(record)

    ikw_kb = types.InlineKeyboardMarkup(row_width=2)
    ikw_kb.add(*buttons1)
    return ikw_kb


def service_key(mr):
    ikw_kb = types.InlineKeyboardMarkup(row_width=2)
    ikw_kb.add(*mr)
    return ikw_kb


def serv_key(mr):
    ikw_kb = types.InlineKeyboardMarkup(row_width=1)
    ikw_kb.add(*mr)
    return ikw_kb
