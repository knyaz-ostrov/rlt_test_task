import json

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart

from data.scripts.bot_data import BotMessageText
from scripts.agregator import Agregator



router = Router()



@router.message(CommandStart())
async def start_cmd(message: Message) -> None:
    await message.answer(BotMessageText.start.format(message.from_user.username))



@router.message(F.text)
async def mes(message: Message) -> None:
    input_data = eval(message.text)
    if type(input_data) != dict:
        await message.answer(BotMessageText.incorrect_request)
        return
    output = json.dumps(Agregator(input_data).output_data)
    await message.answer(output)