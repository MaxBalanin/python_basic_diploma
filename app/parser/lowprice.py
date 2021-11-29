# # -*- coding: UTF-8 -*-
import logging
from aiogram.dispatcher.filters.state import State, StatesGroup
from logging.config import fileConfig
from app.parser.printer_main import Request
from config import BASE_DIR

logging.config.fileConfig(f'{BASE_DIR}/logger/loggingconfig.ini',
                          disable_existing_loggers=False)
logger = logging.getLogger('filelogs')


class LowPrice(Request):
    def __init__(self, user_data):
        super().__init__(user_data)
        self.sortored = 'PRICE'


class HotelConfig(StatesGroup):
    waiting_city_l = State()
    waiting_listsize_l = State()
    waiting_photo_need_l = State()
    waiting_photo_count_l = State()

