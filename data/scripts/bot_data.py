"""
Модуль для текста, который используется в функционале бота
"""
import lxml.etree as ET


FILE_PATH = 'data/data/bot_data.xml'
path_template = './/{}'
filter = '[@id="{}"]'


class BotMessageText:
    """
    Класс для хранения текстовых сообщений отправляемых ботом
    """
    __bot_data = ET.parse(FILE_PATH)
    __category = 'text'
    __path = path_template.format(__category) + filter

    start             = __bot_data.xpath(__path.format('start'))[0].text
    incorrect_request = __bot_data.xpath(__path.format('incorrect_request'))[0].text
