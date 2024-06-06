from datetime import datetime
from dateutil.relativedelta import relativedelta

from database.mongodb import GetData



class Agregator:
    def __init__(self, input_data: dict) -> None:
        self.__input_data = input_data
        self.__time_format = "%Y-%m-%dT%H:%M:%S"

        self.__dt_from = datetime.strptime(input_data['dt_from'], self.__time_format)
        self.__dt_upto = datetime.strptime(input_data['dt_upto'], self.__time_format)
        self.__group_type = self.__input_data['group_type']

        self.__data = GetData(self.__dt_from, self.__dt_upto).result

        self.output_data = {
            'dataset': [0],
            'labels': [self.__dt_from]
        }

        self.__make_labels()
        self.__agregating()
        self.__convert_datetime_to_string()



    def __make_labels(self) -> None:
        '''Занесение всех временных промежутков в output_data'''

        # Определение базовой даты, от которой пойдет занесение дат
        date = datetime(
            *{
            'month': [self.__dt_from.year, self.__dt_from.month, 1],
            'day':   [self.__dt_from.year, self.__dt_from.month, self.__dt_from.day],
            'hour':  [self.__dt_from.year, self.__dt_from.month, self.__dt_from.day, self.__dt_from.hour]
            }[self.__group_type]
        )

        # Словарь для определения крайней даты, на которой нужно остановить процесс
        end_date_types = {
            'month': [self.__dt_upto.year, self.__dt_upto.month, 1],
            'day':   [self.__dt_upto.year, self.__dt_upto.month, self.__dt_upto.day],
            'hour':  [self.__dt_upto.year, self.__dt_upto.month, self.__dt_upto.day, self.__dt_upto.hour]
        }

        # Словарь для определения шага отсчета дат
        relativedelta_types = {
            'month': relativedelta(months=1),
            'day':   relativedelta(days=1),
            'hour':  relativedelta(hours=1)
        }

        while True:
            if date >= datetime(*end_date_types[self.__group_type]):
                break
            date += relativedelta_types[self.__group_type]
            self.output_data['labels'].append(date)
            self.output_data['dataset'].append(0)



    def __agregating(self) -> None:
        '''Агрегация полученных данных из бд'''

        for obj in self.__data:
            for i, dt in enumerate(self.output_data['labels'], 0):
                # Проверяет не выходит ли объект из бд за временные рамки даты из labels
                if {
                    'month': obj['dt'].year != dt.year or obj['dt'].month != dt.month,
                    'day'  : obj['dt'].year != dt.year or obj['dt'].month != dt.month or obj['dt'].day != dt.day,
                    'hour' : obj['dt'].year != dt.year or obj['dt'].month != dt.month or obj['dt'].day != dt.day or obj['dt'].hour != dt.hour
                }[self.__group_type]: continue

                self.output_data['dataset'][i] += obj['value']



    def __convert_datetime_to_string(self):
        for i in range(len(self.output_data['labels'])):
            self.output_data['labels'][i] = self.output_data['labels'][i].strftime(self.__time_format)