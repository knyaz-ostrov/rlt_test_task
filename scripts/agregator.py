"""
Модуль для отправки запроса в MongoDB, агрегации
и возврата полученных данных.
"""
from datetime import datetime

from pymongo.cursor import Cursor
from dateutil.relativedelta import relativedelta

from database.mongodb import MongoDB


class Agregator:
    """
    Класс для агрегации данных.
    """
    def __init__(self, input_data: dict) -> None:
        time_format = "%Y-%m-%dT%H:%M:%S"

        dt_from = datetime.strptime(
            input_data['dt_from'],
            time_format
        )
        dt_upto = datetime.strptime(
            input_data['dt_upto'],
            time_format
        )

        self.output_data = {
            'dataset': [0],
            'labels': [dt_from]
        }

        self.__make_labels(dt_from, dt_upto, input_data['group_type'])
        self.__agregating(MongoDB(dt_from, dt_upto).result, input_data['group_type'])
        self.__convert_datetime_to_string(time_format)

    def __make_labels(self, dt_from: datetime, dt_upto: datetime,
                      group_type: str) -> None:
        """
        Метод для занесения в выходные данные все временные промежутки агрегации данных.
            1. Сначала форматирует стартовую дату исходя из временного диапазона во входных.
               параметрах и типах группировки.
            2. Форматирует конечную дату по принципу из пункта 1.
            3. Определяет размер шага для отсчета заносимых в выходные данные дат.
            4. На основе всех определенных выше параметров заносит все даты с помощью цикла.
        
        :param dt_from: Стартовая дата.
        :param dt_upto: Конечная дата.
        :param group_type: Тип агрегации ('month', 'day', 'hour').
        :return:
        """
        def date_formatting(dt: datetime, group_type: str) -> datetime:
            """
            Форматирует дату по заданному типу группировки.
            
            :param dt: Дата, которую нужно форматировать.
            :param group_type: Тип форматирования ('month', 'day', 'hour').
            :return: Отформатированный объект datetime.
            """
            return datetime(
                *{
                'month': [dt.year, dt.month, 1],
                'day':   [dt.year, dt.month, dt.day],
                'hour':  [dt.year, dt.month, dt.day, dt.hour] 
                }.get(group_type)
            )

        date = date_formatting(dt_from, group_type)
        end_date = date_formatting(dt_upto, group_type)

        date_step = {
            'month': relativedelta(months=1),
            'day':   relativedelta(days=1),
            'hour':  relativedelta(hours=1)
        }.get(group_type)

        while date < end_date:
            date += date_step
            self.output_data['labels'].append(date)
            self.output_data['dataset'].append(0)

    def __agregating(self, data: Cursor, group_type: str) -> None:
        """
        Итерирует все объекты, полученные из MongoDB и сортирует их по соотвествующим объектам.
        выходных данных.
            1. Первый цикл: извлекает объект из данных MongoDB.
            2. Второй цикл: сравнивает его со всеми рассортированными объектами дат в выходных.
               данных.
            3. Заносит данные в нужный объект выходных данных.

        :param data: Объект курсора MongoDB с нужными данными.
        :param group_type: Тип агрегации ('month', 'day', 'hour').
        :return:
        """
        for obj in data:
            for i, dt in enumerate(self.output_data['labels'], 0):
                if {
                    'month': obj['dt'].year != dt.year or obj['dt'].month != dt.month,

                    'day'  : obj['dt'].year != dt.year or obj['dt'].month != dt.month
                             or obj['dt'].day != dt.day,

                    'hour' : obj['dt'].year != dt.year or obj['dt'].month != dt.month
                             or obj['dt'].day != dt.day or obj['dt'].hour != dt.hour
                }.get(group_type): continue

                self.output_data['dataset'][i] += obj['value']

    def __convert_datetime_to_string(self, time_format: str) -> None:
        """
        Конвертирует все объекты datetime в выходных данных в строковый тип.

        :param time_format: Шаблон строки для форматирования.
        :return:
        """
        for i in range(len(self.output_data['labels'])):
            self.output_data['labels'][i] = self.output_data['labels'][i].strftime(time_format)
