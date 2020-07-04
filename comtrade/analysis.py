try:
    from config import *
except ImportError:
    from .config import *

import time

from comtrade.api import Api


class Analysis(object):
    def __init__(self):
        self.api = Api()

    def set_source_destination(self, source, destination):
        self.reporter_area = source
        self.partner_area = destination

    def source_data_available(self, period=2019):
        return self.api.data_available(reporter_area=self.reporter_area, period=period)

    def destination_data_available(self, period=2019):
        return self.api.data_available(reporter_area=self.partner_area, period=period)

    def compare_export(self, period=2019, aggregation = 'AG6', frequency = 'A', classification = 'HS'):
        data_out = self.api.get_data(self.reporter_area, self.partner_area, 2, period = period, aggregation = aggregation, frequency = frequency, classification = classification)  # export
        time.sleep(1)
        data_in = self.api.get_data(self.partner_area, self.reporter_area, 1, period = period, aggregation = aggregation, frequency = frequency, classification = classification)  # import
        return self.compare(data_out, data_in)

    def compare_import(self, period=2019, aggregation = 'AG6', frequency = 'A', classification = 'HS'):
        data_in = self.api.get_data(self.reporter_area, self.partner_area, 1, period = period, aggregation = aggregation, frequency = frequency, classification = classification)  # import
        print(data_in)
        time.sleep(1)
        data_out = self.api.get_data(self.partner_area, self.reporter_area, 2, period = period, aggregation = aggregation, frequency = frequency, classification = classification)  # export
        return self.compare(data_in, data_out)

    def compare(self, data_a, data_b, column='cmdCode'):
        print(data_a)
        input('press ...')
        print(data_b)

        data = {}
        for item in data_a['dataset']:
            if item[column] in data:
                print("Duplicate " + column + " found")
            else:
                net_weight = 0 if item['NetWeight'] is None else item['NetWeight']
                trade_value = 0 if item['TradeValue'] is None else item['TradeValue']
                data[item[column]] = {
                    'code': item['cmdCode'],
                    'desc': item['cmdDescE'],
                    'quantity_a': net_weight,
                    'quantity_desc_a': item['qtDesc'],
                    'value_a': round(trade_value/1000000,2),
                    'quantity_b': 0,
                    'quantity_desc_b': item['qtDesc'],
                    'value_b': 0,
                    # 'quantity_diff': 0,
                    # 'value_diff': 0
                }

        for item in data_b['dataset']:
            net_weight = 0 if item['NetWeight'] is None else item['NetWeight']
            trade_value = 0 if item['TradeValue'] is None else item['TradeValue']
            if item[column] in data:
                data[item[column]].update({
                    'quantity_b': net_weight,
                    'quantity_desc_b': item['qtDesc'],
                    'value_b': round(trade_value/1000000,2),
                    # 'quantity_diff': (data[item['cmdCode']]['quantity_a'] - net_weight),
                    # 'value_diff': (data[item['cmdCode']]['value_a'] - trade_value)
                })
            else:
                data[item[column]] = {
                    'code': item['cmdCode'],
                    'desc': item['cmdDescE'],
                    'quantity_a': 0,
                    'quantity_desc_a': item['qtDesc'],
                    'value_a': 0,
                    'quantity_b': net_weight,
                    'quantity_desc_b': item['qtDesc'],
                    'value_b': round(trade_value/1000000,2),
                    # 'quantity_diff': (0 - net_weight),
                    # 'value_diff': (0 - trade_value)
                }
        return data

