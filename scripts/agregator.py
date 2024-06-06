from datetime import datetime
from dateutil.relativedelta import relativedelta

from database.mongodb import GetData



class Agregator:
    def __init__(self, input_data: dict) -> None:
        self.input_data = input_data
        self.dt_from = self.__convert_to_datetime(input_data['dt_from'])
        self.dt_upto = self.__convert_to_datetime(input_data['dt_upto'])

        self.data = GetData(self.dt_from, self.dt_upto).result

        self.output_data = {
            'dataset': [0],
            'labels': [self.dt_from]
        }
        
        self.__make_labels()
        self.__agregating()
    
    def __convert_to_datetime(self, date: str) -> datetime:
        return datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")

    def __make_labels(self) -> None:
        '''Составление всех временных промежутков'''
        start_date_types = {
            'month': [self.dt_from.year, self.dt_from.month, 1],
            'day':   [self.dt_from.year, self.dt_from.month, self.dt_from.day],
            'hour':  [self.dt_from.year, self.dt_from.month, self.dt_from.day, self.dt_from.hour]
        }
        date = datetime(*start_date_types[self.input_data['group_type']])
        relativedelta_types = {
            'month': relativedelta(months=1),
            'day':   relativedelta(days=1),
            'hour':  relativedelta(hours=1)
        }
        end_date_types = {
            'month': [self.dt_upto.year, self.dt_upto.month, 1],
            'day':   [self.dt_upto.year, self.dt_upto.month, self.dt_upto.day],
            'hour':  [self.dt_upto.year, self.dt_upto.month, self.dt_upto.day, self.dt_upto.hour]
        }
        while True:
            if date >= datetime(*end_date_types[self.input_data['group_type']]):
                break
            date += relativedelta_types[self.input_data['group_type']]
            self.output_data['labels'].append(date)
            self.output_data['dataset'].append(0)

    def __agregating(self) -> None:
        '''Агрегация полученных данных из бд'''
        for obj in self.data:
            for i, dt in enumerate(self.output_data['labels'], 0):
                condition_dict = {
                    'month': obj['dt'].year != dt.year or obj['dt'].month != dt.month,
                    'day'  : obj['dt'].year != dt.year or obj['dt'].month != dt.month or obj['dt'].day != dt.day,
                    'hour' : obj['dt'].year != dt.year or obj['dt'].month != dt.month or obj['dt'].day != dt.day or obj['dt'].hour != dt.hour
                }
                if condition_dict[self.input_data['group_type']]:
                    continue
                self.output_data['dataset'][i] += obj['value']
        
        for i in range(len(self.output_data['labels'])):
            self.output_data['labels'][i] = self.output_data['labels'][i].strftime("%Y-%m-%dT%H:%M:%S")