# # -*- coding: UTF-8 -*-
import logging
from aiogram.dispatcher.filters.state import State, StatesGroup
from logging.config import fileConfig
from app.parser.printer_main import Request
from config import BASE_DIR

logging.config.fileConfig(f'{BASE_DIR}/logger/loggingconfig.ini',
                          disable_existing_loggers=False)
logger = logging.getLogger('filelogs')


class BestDeal(Request):
    def __init__(self, user_data):
        super().__init__(user_data)
        self.sortored = 'PRICE'
        self.pricemin = user_data.get('pricemin')
        self.pricemax = user_data.get('pricemax')
        self.landmark = f"{float(user_data.get('landmark'))} miles"


class HotelConfig(StatesGroup):
    waiting_city_b = State()
    waiting_listsize_b = State()
    waiting_pricemin_b = State()
    waiting_pricemax_b = State()
    waiting_landmark_b = State()
    waiting_photo_need_b = State()
    waiting_photo_count_b = State()

