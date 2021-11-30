# # -*- coding: UTF-8 -*-
import logging
from logging.config import fileConfig

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
import aiogram.utils.markdown as fmt
import json
from datetime import datetime

from app.parser import bestdeal
from database import db
from config import BASE_DIR

logging.config.fileConfig(f'{BASE_DIR}/logger/loggingconfig.ini',
                          disable_existing_loggers=False)
logger = logging.getLogger('filelogs')

hotel_config_l = bestdeal.HotelConfig


async def get_bestdeal_b(message: types.Message):
    logger.info(f'Выполняется функция {__name__}')
    await message.answer('В каком городе смотрим отели? (название города на английском языке)')
    await hotel_config_l.waiting_city_b.set()
    logger.info(f'Функция выполнена {__name__}')


async def set_city_b(message: types.Message, state: FSMContext):
    logger.info(f'Выполняется функция {__name__}')
    await state.update_data(city=message.text.lower())
    await hotel_config_l.next()
    await message.answer('Сколько вариантов показать(максимум 25)')
    logger.info(f'Функция выполнена {__name__}')


async def set_listsize_b(message: types.Message, state: FSMContext):
    logger.info(f'Выполняется функция {__name__}')
    await state.update_data(listsize=message.text)
    await hotel_config_l.next()
    await message.answer('Укажите минимальную цену (USD)')
    logger.info(f'Функция выполнена {__name__}')


async def set_pricemin_b(message: types.Message, state: FSMContext):
    logger.info(f'Выполняется функция {__name__}')
    await state.update_data(pricemin=message.text)
    await hotel_config_l.next()
    await message.answer('Укажите максимальную цену (USD)')
    logger.info(f'Функция выполнена {__name__}')


async def set_pricemax_b(message: types.Message, state: FSMContext):
    logger.info(f'Выполняется функция {__name__}')
    await state.update_data(pricemax=message.text)
    await hotel_config_l.next()
    await message.answer('Укажите максимальную дистанцию до центра города.')
    logger.info(f'Функция выполнена {__name__}')


async def set_landmark_b(message: types.Message, state: FSMContext):
    logger.info(f'Выполняется функция {__name__}')
    await state.update_data(landmark=message.text)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    var = ['Да', 'Нет']
    for ans in var:
        keyboard.add(ans)
    await hotel_config_l.next()
    await message.answer('Нужны фото отелей?', reply_markup=keyboard)
    logger.info(f'Функция выполнена {__name__}')


async def set_photo_need_b(message: types.Message, state: FSMContext):
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
            result = bestdeal.BestDeal(user_data).print()
            db.set_history_db(message.from_user.id, json.dumps(result),
                              datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M'), '/bestdeal')
            for i in result:
                await message.answer(f"Название: {i['hotel name']}\n"
                                     f"Адрес: {i['hotel address']}\n"
                                     f"Расстояние до центра: {i['hotel landmarks distance']}\n"
                                     f"Цена: {i['price']}")
            await state.finish()
            logger.info(f'Функция выполнена {__name__}')
        except Exception as e:
            logger.warning(f'Ошибка при выполнении функции {e}')
            await message.answer('Произошла ошибка, попробуйте снова!\n/bestdeal')
            await state.finish()


async def set_photo_count_b(message: types.Message, state: FSMContext):
    logger.info(f'Выполняется функция {__name__}')
    await state.update_data(photo_count=message.text)
    user_data = await state.get_data()
    result = bestdeal.BestDeal(user_data).print()
    db.set_history_db(message.from_user.id, json.dumps(result),
                      datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M'), '/bestdeal')
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
        await message.answer('Произошла ошибка, попробуйте снова!\n/bestdeal')
        await state.finish()


async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Действие отменено", reply_markup=types.ReplyKeyboardRemove())


def register_bestdeal(dp: Dispatcher):
    logger.info(f'Выполняется функция ')
    dp.register_message_handler(get_bestdeal_b, commands="bestdeal", state="*")
    dp.register_message_handler(cmd_cancel, commands="cancel", state="*")
    dp.register_message_handler(set_city_b, state=hotel_config_l.waiting_city_b)
    dp.register_message_handler(set_listsize_b, state=hotel_config_l.waiting_listsize_b)
    dp.register_message_handler(set_pricemin_b, state=hotel_config_l.waiting_pricemin_b)
    dp.register_message_handler(set_pricemax_b, state=hotel_config_l.waiting_pricemax_b)
    dp.register_message_handler(set_landmark_b, state=hotel_config_l.waiting_landmark_b)
    dp.register_message_handler(set_photo_need_b, state=hotel_config_l.waiting_photo_need_b)
    dp.register_message_handler(set_photo_count_b, state=hotel_config_l.waiting_photo_count_b)
    logger.info(f'Функция выполнена {__name__}')

