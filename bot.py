"""
Модуль для непосредственного запуска бота.
"""
import asyncio
import logging

from aiogram import Bot, Dispatcher

from handlers import general
from data.scripts.config import BotConfig


async def main() -> None:
    """
    Устанавливает токен для бота,
    добавляет роутеры из каталога
    handlers, удаляет все входящие
    события, поступившие в момент
    неактивности бота. Запускает бота.

    :return:
    """
    bot = Bot(BotConfig.token)

    dp = Dispatcher()
    dp.include_router(general.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


def logger() -> None:
    """
    Настройка логгирования.

    :return:
    """
    logging.basicConfig(
        level=logging.INFO,
        filename="log.log",
        filemode="w",
        format="%(asctime)s %(levelname)s %(message)s",
        encoding='UTF-8'
    )


if __name__ == '__main__':
    logger()            # Запуск и настройка логгирования.
    asyncio.run(main()) # Запуск бота.
