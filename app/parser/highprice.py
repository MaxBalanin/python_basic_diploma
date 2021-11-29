# # -*- coding: UTF-8 -*-
import logging
from logging.config import fileConfig
from aiogram.dispatcher.filters.state import State, StatesGroup
from app.parser.printer_main import Request
from config import BASE_DIR

logging.config.fileConfig(f'{BASE_DIR}/logger/loggingconfig.ini',
                          disable_existing_loggers=False)
logger = logging.getLogger('filelogs')


class HighPrice(Request):
    def __init__(self, user_data):
        super().__init__(user_data)
        self.sortored = 'PRICE_HIGHEST_FIRST'


class HotelConfig(StatesGroup):
    waiting_city_h = State()
    waiting_listsize_h = State()
    waiting_photo_need_h = State()
    waiting_photo_count_h = State()

