# # -*- coding: UTF-8 -*-
import sqlite3

import logging
from logging.config import fileConfig
from config import BASE_DIR

logging.config.fileConfig(f'{BASE_DIR}/logger/loggingconfig.ini',
                          disable_existing_loggers=False)
logger = logging.getLogger('filelogs')


def create_table():
    """
    Подключается к базе и создаёт таблицы city_id и history если их не существует
    :return:
    """
    with sqlite3.connect(f'{BASE_DIR}/database/database.db') as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS city_id(city, id)')
        conn.commit()
        conn.execute('CREATE TABLE IF NOT EXISTS history(user_id, history, date, command)')
        conn.commit()


def set_city_id_db(city: str, city_id: str):
    """
    Подключается к базе и добавляет в таблиц city_id город и его ИД
    :return:
    """
    with sqlite3.connect(f'{BASE_DIR}/database/database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO city_id VALUES(?, ?)', (city, city_id))
        conn.commit()


def get_citi_id_db(city: str):
    """
    Подключается к базе и Возвращает ИД города если есть, None если города нет
    :return:
    """
    with sqlite3.connect(f'{BASE_DIR}/database/database.db') as conn:
        cursor = conn.cursor()
        data = cursor.execute('SELECT * FROM city_id').fetchall()
        for i in data:
            if i[0] == city:
                return i[1]
        else:
            return None


def set_history_db(user_id: int, hist: str, date: str, command: str):
    """
    Подключается к базе и добавляет в таблиц history ИД_юзера, запрос, дату запроса и Команду
    :return:
    """
    with sqlite3.connect(f'{BASE_DIR}/database/database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO history VALUES(?, ?, ?, ?)',
                       (user_id, hist, date, command))
        conn.commit()


def get_history_db(user_id: int):
    """
    Подключается к базе и возвразает список словарей с историй запросов пользователя
    :param user_id: ИД_юзера
    :return: Список словарей
    """
    with sqlite3.connect(f'{BASE_DIR}/database/database.db') as conn:
        cursor = conn.cursor()
        data = cursor.execute('SELECT * FROM history WHERE user_id = {}'.format(user_id)).fetchall()
        return data


def delete_history(user_id: int):
    """
    Подключается к базе и удаляет историю запросов пользователя
    :param user_id: ИД_юзера
    :return:
    """
    with sqlite3.connect(f'{BASE_DIR}/database/database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM history WHERE user_id = {}'.format(user_id))
        conn.commit()


create_table()
