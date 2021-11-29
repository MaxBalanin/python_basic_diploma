# graduation project


##app/parser

###request_main
####request_main
Выполняет запрос к api properties/list и возвращает список отелей по заданным параметрам 
####get_photo_list 
Выполняет запрос к api properties/get-hotel-photos и возвращает список фото отелей по заданным параметрам 
####get_city_id
Проверяет наличие города в базе данных, если нет, то выполняет запрос к api properties/v2/search, возвращает id города

###printer_main
####class Request
Экземпляр класса содержит параметры для выполнения запроса request_main, полученные из данных пользователя
####request
Выполняет запрос request_main с заданными параметрами и возвращает ответ
####print
Создаёт и возвращает список отелей с нужными данными из запроса request (и при необходимости get_photo_list) 

###lowprice
Переопределят класс Request\
Содержит класс HotelConfig, наследуемый от StatesGroup для машины состояний cmd_lowprice

###highprice
Переопределят класс Request\
Содержит класс HotelConfig, наследуемый от StatesGroup для машины состояний cmd_highprice

###bestdeal
Переопределят класс Request\
Содержит класс HotelConfig, наследуемый от StatesGroup для машины состояний cmd_bestdeal

##app/handlers
###cmd_lowprice
Содержит машину состояний для команды /lowprice, собирает данные от пользователя, выполняет запрос
lowprice и отправляет пользователю сообщение с ответом

###cmd_highprice
Содержит машину состояний для команды /lowprice, собирает данные от пользователя, выполняет запрос
lowprice и отправляет пользователю сообщение с ответом

###cmd_bestdeal
Содержит машину состояний для команды /lowprice, собирает данные от пользователя, выполняет запрос
lowprice и отправляет пользователю сообщение с ответом(добавляет полученный ответ в базу данных)
###common
Содержит команды /start /help и /cancel
###cmd_history
Содержит команду set_history для выдачи пользователю истории и команду clear_history для удаления истории пользователя

##database
###db
Содержит команды:\
create_table - создаёт таблицу городов и истории, если их не существует\
set_city_id_db - добавляет id города в базу данных\
get_citi_id_db - получает id города из базы данных\
set_history_db - добавляет запрос в историю пользователя\
get_history_db - получает историю запросов из базы данных\
delete_history - удаляет из базы данных историю пользователя

##logger
Содержит файл loggingconfig.ini с конфигурацией логгера


