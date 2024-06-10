"""
Модуль для извлечения конфигурационных файлов
из json-файла.
"""
import json


FILE_PATH = 'data/data/config.json'


class BotConfig:
    """
    Класс для хранения конфигурационных
    данных бота.
    """
    with open(FILE_PATH, encoding='UTF-8') as file:
        __bot_config = json.load(file)['bot']

    token = __bot_config['token']


class MongoConfig:
    """
    Класс для хранения конфигурационных данных
    MongoDB.
    """
    with open(FILE_PATH, encoding='UTF-8') as file:
        __mongo_config = json.load(file)['mongodb']

    database   = __mongo_config['database']
    collection = __mongo_config['collection']
