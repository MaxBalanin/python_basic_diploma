# # -*- coding: UTF-8 -*-
import sqlite3

import logging
from logging.config import fileConfig
from config import BASE_DIR

logging.config.fileConfig(f'{BASE_DIR}/logger/loggingconfig.ini',
                          disable_existing_loggers=False)
logger = logging.getLogger('filelogs')


def create_table():
    with sqlite3.connect(f'{BASE_DIR}/database/database.db') as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS city_id(city, id)')
        conn.commit()
        conn.execute('CREATE TABLE IF NOT EXISTS history(user_id, history, date, command)')
        conn.commit()


def set_city_id_db(city, city_id):
    with sqlite3.connect(f'{BASE_DIR}/database/database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO city_id VALUES(?, ?)', (city, city_id))
        conn.commit()


def get_citi_id_db(city):
    with sqlite3.connect(f'{BASE_DIR}/database/database.db') as conn:
        cursor = conn.cursor()
        data = cursor.execute('SELECT * FROM city_id').fetchall()
        for i in data:
            if i[0] == city:
                return i[1]
        else:
            return None


def set_history_db(user_id, hist, date, command):
    with sqlite3.connect(f'{BASE_DIR}/database/database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO history VALUES(?, ?, ?, ?)',
                       (user_id, hist, date, command))
        conn.commit()


def get_history_db(user_id):
    with sqlite3.connect(f'{BASE_DIR}/database/database.db') as conn:
        cursor = conn.cursor()
        data = cursor.execute('SELECT * FROM history WHERE user_id = {}'.format(user_id)).fetchall()
        return data


def delete_history(user_id):
    with sqlite3.connect(f'{BASE_DIR}/database/database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM history WHERE user_id = {}'.format(user_id))
        conn.commit()


create_table()
