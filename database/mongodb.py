from datetime import datetime

import pymongo

from data.scripts.config import MongoConfig



class GetData:
    def __init__(self, dt_from: datetime, dt_upto: datetime) -> None:
        self.__database_name = MongoConfig.database
        self.__collection_name = MongoConfig.collection
        self.__dt_from, self.__dt_upto = dt_from, dt_upto
        self.__connect()
        self.__parse()

    def __connect(self) -> None:
        self.__client = pymongo.MongoClient()
        self.__collection = self.__client[f'{self.__database_name}'].get_collection(self.__collection_name)

    def __parse(self) -> None:
        query = {"dt": {'$gte': self.__dt_from, '$lte': self.__dt_upto}}
        self.result = self.__collection.find(query)