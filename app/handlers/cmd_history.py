# # -*- coding: UTF-8 -*-
import logging
from logging.config import fileConfig

import json
from aiogram import Dispatcher, types
from database import db
from config import BASE_DIR

logging.config.fileConfig(f'{BASE_DIR}/logger/loggingconfig.ini',
                          disable_existing_loggers=False)
logger = logging.getLogger('filelogs')


async def set_history(message: types.Message):
    logger.info(f'Выполняется функция ')
    try:
        history = db.get_history_db(message.from_user.id)
        if not history:
            await message.answer('Истории пока нет.')
        for req in history:
            hotels = ''
            for i in json.loads(req[1]):
                hotels += f'\t{i["hotel name"]}\n'
            await message.answer(f'Команда: {req[3]} {req[2]}\n'
                                 f'Город: {json.loads(req[1])[0]["city"]}\n'
                                 f'Отели: \n{hotels}')
        logger.info(f'Функция выполнена ')
    except Exception as e:
        logger.warning(f'Ошибка при выполнении функции {e}')
        await message.answer('Произошла ошибка, попробуйте снова!\n/history')


async def clear_history(message: types.Message):
    db.delete_history(message.from_user.id)
    await message.answer('История очищена.')


def register_history(dp: Dispatcher):
    logger.info(f'Выполняется функция ')
    dp.register_message_handler(set_history, commands="history")
    dp.register_message_handler(clear_history, commands='history_clear')
    logger.info(f'Функция выполнена ')


