# # -*- coding: UTF-8 -*-
import logging
from logging.config import fileConfig

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
import aiogram.utils.markdown as fmt
import json
from datetime import datetime

from app.parser import highprice
from database import db
from config import BASE_DIR


logging.config.fileConfig(f'{BASE_DIR}/logger/loggingconfig.ini',
                          disable_existing_loggers=False)
logger = logging.getLogger('filelogs')

hotel_config_h = highprice.HotelConfig


async def get_highprise_h(message: types.Message):
    logger.info(f'Выполняется функция {__name__}')
    await message.answer('В каком городе смотрим отели? (название города на английском языке)')
    await hotel_config_h.waiting_city_h.set()
    logger.info(f'Функция выполнена {__name__}')


async def set_city_h(message: types.Message, state: FSMContext):
    logger.info(f'Выполняется функция {__name__}')
    await state.update_data(city=message.text.lower())
    await hotel_config_h.next()
    await message.answer('Сколько вариантов показать(максимум 25)')
    logger.info(f'Функция выполнена {__name__}')


async def set_listsize_h(message: types.Message, state: FSMContext):
    logger.info(f'Выполняется функция {__name__}')
    await state.update_data(listsize=message.text)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    var = ['Да', 'Нет']
    for ans in var:
        keyboard.add(ans)
    await hotel_config_h.next()
    await message.answer('Нужны фото отелей?', reply_markup=keyboard)
    logger.info(f'Функция выполнена {__name__}')


async def set_photo_need_h(message: types.Message, state: FSMContext):
    logger.info(f'Выполняется функция {__name__}')
    if message.text not in ['Да', 'Нет']:
        await message.answer('Нужны фото отелей?')
        return
    await state.update_data(photo_need=message.text)

    if message.text == 'Да':
        await hotel_config_h.next()
        await message.answer('Сколько фото показать(максимум 5)', reply_markup=types.ReplyKeyboardRemove())
    else:
        try:
            await message.answer('Отлично, ожидайте!', reply_markup=types.ReplyKeyboardRemove())
            user_data = await state.get_data()
            user_data['photo_count'] = '0'
            result = highprice.HighPrice(user_data).print()
            db.set_history_db(message.from_user.id, json.dumps(result),
                              datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M'), '/highprice')
            for i in result:
                await message.answer(f"Название: {i['hotel name']}\n"
                                     f"Адрес: {i['hotel address']}\n"
                                     f"Расстояние до центра: {i['hotel landmarks distance']}\n"
                                     f"Цена: {i['price']}")
            await state.finish()
            logger.info(f'Функция выполнена {__name__}')
        except Exception as e:
            logger.warning(f'Ошибка при выполнении функции {e}')
            await message.answer('Произошла ошибка, попробуйте снова!\n/highprice')
            await state.finish()


async def set_photo_count_h(message: types.Message, state: FSMContext):
    logger.info(f'Выполняется функция {__name__}')
    await state.update_data(photo_count=message.text)
    user_data = await state.get_data()

    result = highprice.HighPrice(user_data).print()
    db.set_history_db(message.from_user.id, json.dumps(result),
                      datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M'), '/highprice')
    try:
        for i in result:
            await message.answer(f"{i['hotel name']}\n"
                                 f"{i['hotel address']}\n"
                                 f"{i['hotel landmarks distance']}\n"
                                 f"{i['price']}")
            for j in i['photo']:
                await message.answer(fmt.hide_link(j), parse_mode=types.ParseMode.HTML)
        await state.finish()
        logger.info(f'Функция выполнена {__name__}')
    except Exception as e:
        logger.warning(f'Ошибка при выполнении функции {e}')
        await message.answer('Произошла ошибка, попробуйте снова!\n/highprice')
        await state.finish()


def register_highprice(dp: Dispatcher):
    logger.info(f'Выполняется функция ')
    dp.register_message_handler(get_highprise_h, commands="highprice", state="*")
    dp.register_message_handler(set_city_h, state=hotel_config_h.waiting_city_h)
    dp.register_message_handler(set_listsize_h, state=hotel_config_h.waiting_listsize_h)
    dp.register_message_handler(set_photo_need_h, state=hotel_config_h.waiting_photo_need_h)
    dp.register_message_handler(set_photo_count_h, state=hotel_config_h.waiting_photo_count_h)
    logger.info(f'Функция выполнена {__name__}')

