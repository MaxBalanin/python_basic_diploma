# # -*- coding: UTF-8 -*-
import logging
from logging.config import fileConfig
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import token, BASE_DIR

from app.handlers.cmd_lowprice import register_lowprice
from app.handlers.cmd_history import register_history
from app.handlers.cmd_highprice import register_highprice
from app.handlers.cmd_bestdeal import register_bestdeal
from app.handlers.common import register_handlers_common


logging.config.fileConfig(f'{BASE_DIR}/logger/loggingconfig.ini',
                          disable_existing_loggers=False)
logger = logging.getLogger('filelogs')


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/lowprice", description="Узнать топ самых дешёвых отелей в городе."),
        BotCommand(command="/highprice", description="Узнать топ самых дорогих отелей в городе."),
        BotCommand(command="/bestdeal", description="Узнать топ отелей, наиболее подходящих"
                                                    " по цене и расположению от центра"),
        BotCommand(command="/history", description="Посмотреть историю запросов."),
        BotCommand(command="/history_clear", description="Очистить историю запросов."),
        BotCommand(command="/cancel", description="Отмена команды.")
    ]
    await bot.set_my_commands(commands)


async def main():
    logger.warning("Starting bot")

    bot = Bot(token=token)
    dp = Dispatcher(bot, storage=MemoryStorage())

    register_highprice(dp)
    register_lowprice(dp)
    register_history(dp)
    register_bestdeal(dp)
    register_handlers_common(dp)

    await set_commands(bot)
    await dp.start_polling()


if __name__ == "__main__":
    asyncio.run(main())
