import requests
import logging
from logging.config import fileConfig
from datetime import datetime
import json

from config import headers as head
from database.db import set_city_id_db, get_citi_id_db
from config import BASE_DIR

logging.config.fileConfig(f'{BASE_DIR}/python_basic_diploma/logger/loggingconfig.ini',
                          disable_existing_loggers=False)
logger = logging.getLogger('filelogs')


def get_city_id(city_name):
    logger.info(f'Выполняется функция с аргументами  {city_name}')
    try:
        city_id = get_citi_id_db(city_name.lower())
        if city_id is not None:
            return city_id
        else:
            url = "https://hotels4.p.rapidapi.com/locations/v2/search"
            querystring = {f"query": {city_name}, "currency": "USD"}
            headers = head
            response = requests.request("GET", url, headers=headers, params=querystring)
            data = json.loads(response.text)
            city_id = data["suggestions"][0]["entities"][0]["destinationId"]
            set_city_id_db(city_name.lower(), city_id)
            logger.info(f'Функция выполнена')
            return city_id
    except Exception as e:
        logger.warning(f'Ошибка при выполнении функции - {e} с аргументами  {city_name}')


def get_photo_list(id_hotel, count):
    logger.info(f'Выполняется функция с аргументами id_hotel={id_hotel} count={count}')
    try:
        url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"
        querystring = {"id": id_hotel}
        headers = head
        response = requests.request("GET", url, headers=headers, params=querystring)
        data = json.loads(response.text)
        photo_list = []
        for i in data["hotelImages"]:
            photo = i["baseUrl"].replace('{size}', 'z')
            photo_list.append(photo)
            if len(photo_list) == int(count):
                break
        logger.info(f'Функция выполнена')
        return photo_list
    except Exception as e:
        logger.warning(f'Ошибка при выполнении функции - {e} с аргументами id_hotel={id_hotel} count={count}')


def request_main(city_name='london', listsize='25', sortorder='PRICE',
                 landmark=None, pricemin=None, pricemax=None):
    logger.info(f'Выполняется функция с аргументами city={city_name} listsize={listsize}'
                f' landmark={landmark} pricemin={pricemin} pricemax={pricemax}')
    try:
        request_list = []
        url = "https://hotels4.p.rapidapi.com/properties/list"
        querystring = {f"destinationId": {get_city_id(city_name)},
                       "pageNumber": "1",
                       "pageSize": {listsize},
                       "checkIn": datetime.strftime(datetime.now(), '%Y-%m-%d'),
                       "checkOut": datetime.strftime(datetime.now(), '%Y-%m-%d'),
                       "adults1": "1",
                       "sortOrder": {sortorder},
                       "currency": "USD",
                       "landmarkIds": {landmark},
                       "priceMin": {pricemin},
                       "priceMax": {pricemax}
                       }
        headers = head
        response = requests.request("GET", url, headers=headers, params=querystring)
        data = json.loads(response.text)
        for i in data['data']['body']["searchResults"]["results"]:
            request_list.append(i)
        logger.info(f'Функция выполнена ')
        return request_list
    except Exception as e:
        logger.warning(f'Ошибка при выполнении функции - {e} с аргументами city={city_name} listsize={listsize}'
                       f' landmark={landmark} pricemin={pricemin} pricemax={pricemax}')
        return None


