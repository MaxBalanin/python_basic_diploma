import requests
import logging
from logging.config import fileConfig
from datetime import datetime
import json

from config import headers as head
from database.db import set_city_id_db, get_citi_id_db
from config import BASE_DIR

logging.config.fileConfig(f'{BASE_DIR}/logger/loggingconfig.ini',
                          disable_existing_loggers=False)
logger = logging.getLogger('filelogs')


def get_city_id(city_name: str) -> str:
    '''
    Проверяет наличие города в базе данных, если нет, то выполняет запрос к api properties/v2/search, возвращает id города
    :param city_name название города
    :return id города
    '''
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


def get_photo_list(id_hotel: str, count: str) -> list:
    '''
    Выполняет запрос к api properties/get-hotel-photos и возвращает список фото отелей по заданным параметрам
    :param id_hotel id отеля для поиска
    :param count количество фотографий
    :return список ссылок на фото отеля
    '''
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


def request_main(city_name: str = 'london', listsize: str = '25', sortorder: str = 'PRICE',
                 landmark: str = None, pricemin: str = None, pricemax: str = None):
    '''
    Выполняет запрос к api properties/list и возвращает список отелей по заданным параметрам
    :param city_name название города для поиска
    :param listsize количество отелей
    :param sortorder тип сортировки по цене
    :param landmark дистанция до центра
    :param pricemin минимальная цена
    :param pricemax максимальная цена
    :return список словарей с данными по отелям
    '''
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
