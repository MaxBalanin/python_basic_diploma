# # -*- coding: UTF-8 -*-
import logging
from logging.config import fileConfig

from aiogram import Dispatcher, types
from config import BASE_DIR

logging.config.fileConfig(f'{BASE_DIR}/logger/loggingconfig.ini',
                          disable_existing_loggers=False)
logger = logging.getLogger('filelogs')


async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! Я бот сайта hotels.com и помогу подобрать отель для отдыха в любой точке мира!\n\n"
        "/lowprice - самые дешевые отели\n"
        "/highprice - самые дорогие отели\n"
        "/bestdeal - лучшее предложение\n"
        "/history - история поиска\n"
        "\n Подробная информация по команде /help",
        reply_markup=types.ReplyKeyboardRemove()
    )


async def helper(message: types.Message):
    await message.answer(
        "/lowprice - Узнать топ самых дешёвых отелей в городе.\n"
        "/highprice - Узнать топ самых дорогих отелей в городе.\n"
        "/bestdeal - Узнать топ отелей, наиболее подходящих по цене и расположению от центра.\n"
        "/history - Посмотреть историю запросов.\n"
        "/history_clear - Очистить историю запросов.\n"
        "/cancel -  Отмена команды.",
        reply_markup=types.ReplyKeyboardRemove()
    )


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start")
    dp.register_message_handler(helper, commands="help")


