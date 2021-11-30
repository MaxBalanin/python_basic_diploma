# # -*- coding: UTF-8 -*-
import logging
from logging.config import fileConfig

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
import aiogram.utils.markdown as fmt
import json
from datetime import datetime

from app.parser import lowprice
from database import db
from config import BASE_DIR

logging.config.fileConfig(f'{BASE_DIR}/logger/loggingconfig.ini',
                          disable_existing_loggers=False)
logger = logging.getLogger('filelogs')

hotel_config_l = lowprice.HotelConfig


async def get_lowprice_l(message: types.Message):
    logger.info(f'Выполняется функция {__name__}')
    await message.answer('В каком городе смотрим отели? (название города на английском языке)')
    await hotel_config_l.waiting_city_l.set()
    logger.info(f'Функция выполнена {__name__}')


async def set_city_l(message: types.Message, state: FSMContext):
    logger.info(f'Выполняется функция {__name__}')
    await state.update_data(city=message.text.lower())
    await hotel_config_l.next()
    await message.answer('Сколько вариантов показать(максимум 25)')
    logger.info(f'Функция выполнена {__name__}')


async def set_listsize_l(message: types.Message, state: FSMContext):
    logger.info(f'Выполняется функция {__name__}')
    await state.update_data(listsize=message.text)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    var = ['Да', 'Нет']
    for ans in var:
        keyboard.add(ans)
    await hotel_config_l.next()
    await message.answer('Нужны фото отелей?', reply_markup=keyboard)
    logger.info(f'Функция выполнена {__name__}')


async def set_photo_need_l(message: types.Message, state: FSMContext):
    logger.info(f'Выполняется функция {__name__}')
    if message.text not in ['Да', 'Нет']:
        await message.answer('Нужны фото отелей?')
        return
    await state.update_data(photo_need=message.text)

    if message.text == 'Да':
        await hotel_config_l.next()
        await message.answer('Сколько фото показать(максимум 5)', reply_markup=types.ReplyKeyboardRemove())
    else:
        try:
            await message.answer('Отлично, ожидайте!', reply_markup=types.ReplyKeyboardRemove())
            user_data = await state.get_data()
            user_data['photo_count'] = '0'
            result = lowprice.LowPrice(user_data).print()
            db.set_history_db(message.from_user.id, json.dumps(result),
                              datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M'), '/lowprice')
            for i in result:
                await message.answer(f"Название: {i['hotel name']}\n"
                                     f"Адрес: {i['hotel address']}\n"
                                     f"Расстояние до центра: {i['hotel landmarks distance']}\n"
                                     f"Цена: {i['price']}")
            await state.finish()
            logger.info(f'Функция выполнена {__name__}')
        except Exception as e:
            logger.warning(f'Ошибка при выполнении функции {e}')
            await message.answer('Произошла ошибка, попробуйте снова!\n/lowprice')
            await state.finish()


async def set_photo_count_l(message: types.Message, state: FSMContext):
    logger.info(f'Выполняется функция {__name__}')
    await state.update_data(photo_count=message.text)
    user_data = await state.get_data()
    result = lowprice.LowPrice(user_data).print()
    db.set_history_db(message.from_user.id, json.dumps(result),
                      datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M'), '/lowprice')
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
        await message.answer('Произошла ошибка, попробуйте снова!\n/lowprice')
        await state.finish()


async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Действие отменено", reply_markup=types.ReplyKeyboardRemove())


def register_lowprice(dp: Dispatcher):
    logger.info(f'Выполняется функция ')
    dp.register_message_handler(get_lowprice_l, commands="lowprice", state="*")
    dp.register_message_handler(cmd_cancel, commands="cancel", state="*")
    dp.register_message_handler(set_city_l, state=hotel_config_l.waiting_city_l)
    dp.register_message_handler(set_listsize_l, state=hotel_config_l.waiting_listsize_l)
    dp.register_message_handler(set_photo_need_l, state=hotel_config_l.waiting_photo_need_l)
    dp.register_message_handler(set_photo_count_l, state=hotel_config_l.waiting_photo_count_l)

    logger.info(f'Функция выполнена {__name__}')

