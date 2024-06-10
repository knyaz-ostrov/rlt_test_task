"""
Модуль содержит в себе хандлеры для взаимодействия с ботом.
"""
import json

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart

from scripts.agregator import Agregator
from data.scripts.bot_data import BotMessageText


router = Router()


@router.message(CommandStart())
async def start_cmd(message: Message) -> None:
    """
    Хандлер, реагирует на комманду /start и
    отправляет приветственное сообщение в ответ.

    :param message: Объект Message c данными о событии.
    :return:
    """
    await message.answer(BotMessageText.start.format(message.from_user.username))


@router.message(F.text)
async def text_message(message: Message) -> None:
    """
    Хандлер, реагируюет на любые текстовые сообщения
    и проверяет содержание в них JSON-данных. Если в
    сообщении от пользователя содержится JSON,
    передает его в объект Agregation для получения
    агрегированных данных и отправки их пользователю
    в ответ.

    :param message: Объект Message c данными о событии.
    :return:
    """
    input_data = eval(message.text)
    if type(input_data) != dict:
        await message.answer(BotMessageText.incorrect_request)
        return

    output = json.dumps(Agregator(input_data).output_data)
    await message.answer(output)
