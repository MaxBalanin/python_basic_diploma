# # -*- coding: UTF-8 -*-
import logging
from logging.config import fileConfig
from app.parser.request_main import request_main, get_photo_list
from config import BASE_DIR

logging.config.fileConfig(f'{BASE_DIR}/logger/loggingconfig.ini',
                          disable_existing_loggers=False)
logger = logging.getLogger('filelogs')


class Request:
    '''
    Класс является связующим звеном между парсером api и ботом
    Метод __init__ переопределяется в дочерник классах исходя их их нужд
    '''
    def __init__(self, user_data: dict):
        '''
        Экземпляр класса содержит параметры для выполнения запроса request_main, полученные из данных пользователя
        :param city_name название города для поиска
        :param listsize количество отелей
        :param sortorder тип сортировки по цене
        :param landmark дистанция до центра
        :param pricemin минимальная цена
        :param pricemax максимальная цена
        '''
        self.city = user_data['city']
        self.listsize = user_data['listsize']
        self.photo_need = user_data['photo_need']
        self.photo_count = user_data['photo_count']
        self.pricemin = None
        self.pricemax = None
        self.landmark = None
        self.sortored = ''

    def request(self):
        '''
        Проверяет на корректность данные и выполняет request_main
        :return: список отелей из метода request_main
        '''
        if int(self.listsize) > 25: self.listsize = '25'
        if int(self.photo_count) > 5: self.photo_count = '5'
        request = request_main(city_name=self.city, listsize=self.listsize, sortorder=self.sortored,
                                    landmark=self.landmark, pricemax=self.pricemax, pricemin=self.pricemin)
        return request

    def print(self) ->list:
        '''
        Выбирает из request_main запроса нужные данные для отправки пользователю и возвращает их список
        :return: Спписок словарей с информацией об отелях для отправки пользователю
        '''
        try:
            result_list = []
            j = 0
            for i in self.request():
                result_list.append({})
                result_list[j]['city'] = self.city.capitalize()
                result_list[j]['hotel name'] = (i.get('name'))
                result_list[j]['hotel address'] = (i.get('address').get('streetAddress'))
                result_list[j]['hotel landmarks distance'] = (i.get('landmarks')[0].get('distance'))
                result_list[j]['price'] = (i.get('ratePlan').get('price').get('current'))
                if self.photo_need == 'Да':
                    result_list[j]['photo'] = (get_photo_list(i['id'], self.photo_count))
                j += 1
            logger.info(f'Функция выполнена')
            return result_list
        except Exception as e:
            logger.warning(f'Ошибка при выполнении функции - {e} с аргументами')
