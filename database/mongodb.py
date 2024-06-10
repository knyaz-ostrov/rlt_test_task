"""
Модуль для работы с MongoDB.
"""
from datetime import datetime

import pymongo
from pymongo.cursor import Cursor
from pymongo.collection import Collection

from data.scripts.config import MongoConfig


class MongoDB:
    """
    Класс для извлечения данных из MongoDB в соответствии с
    переданным запросом.
    """
    def __init__(self, dt_from: datetime, dt_upto: datetime) -> None:
        collection = self.__get_collection(MongoConfig.database, MongoConfig.collection)

        self.result = self.__get_data(dt_from, dt_upto, collection)

    def __get_collection(self, database_name: str, collection_name: str) -> Collection:
        """
        Метод подключается к MongoDB и возвращает коллекцию.

        :param database_name: Название базы данных MongoDB.
        :param collection_name: Название коллекции MongoDB.
        :return: Объект Collection.
        """
        client = pymongo.MongoClient()
        return client[f'{database_name}'].get_collection(collection_name)

    def __get_data(self, dt_from: datetime, dt_upto: datetime, collection: Collection) -> Cursor:
        """
        Метод ищет в коллекции все объекты, в которых параметр dt соответствует переданному
        диапазону дат.

        :param dt_from: Начальная дата поиска.
        :param dt_upto: Конечная дата поиска.
        :param collection: Коллекция, в которой будет осуществляться поиск.
        :return: Объект Cursor, хранящий в себе подходящие объекты.
        """
        return collection.find({"dt": {'$gte': dt_from, '$lte': dt_upto}})
