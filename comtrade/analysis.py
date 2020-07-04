try:
    from config import *
except ImportError:
    from .config import *

import time
import pandas as pd
from comtrade.api import Api


class Analysis(object):
    def __init__(self):
        self.api = Api()

    def data_available(self, reporter_area, period=2019, classification = 'HS', frequency = 'A'):
        return self.api.data_available(reporter_area, period, classification, frequency)

    def get_export_data(self, reporter_area, partner_area, period=2019, aggregation = 'AG6', frequency = 'A', classification = 'HS'):
        data_out = self.api.get_data(reporter_area, partner_area, 2, period = period, aggregation = aggregation, frequency = frequency, classification = classification)  # export
        time.sleep(1)
        data_in = self.api.get_data(partner_area, reporter_area, 1, period = period, aggregation = aggregation, frequency = frequency, classification = classification)  # import
        return data_out, data_in

    def get_import_data(self, reporter_area, partner_area, period=2019, aggregation = 'AG6', frequency = 'A', classification = 'HS'):
        data_in = self.api.get_data(reporter_area, partner_area, 1, period = period, aggregation = aggregation, frequency = frequency, classification = classification)  # import
        time.sleep(1)
        data_out = self.api.get_data(partner_area, reporter_area, 2, period = period, aggregation = aggregation, frequency = frequency, classification = classification)  # export
        return data_in, data_out

    def compare(self, data_a, data_b, column_a='cmdCode', column_b='cmdCode'):

        data = {}
        for item in data_a['dataset']:
            if item[column_a] in data:
                print("Duplicate " + column_a + " found")
            else:
                net_weight = 0 if item['NetWeight'] is None else item['NetWeight']
                trade_value = 0 if item['TradeValue'] is None else item['TradeValue']
                data[item[column_a]] = {
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
            if item[column_b] in data:
                data[item[column_b]].update({
                    'quantity_b': net_weight,
                    'quantity_desc_b': item['qtDesc'],
                    'value_b': round(trade_value/1000000,2),
                    # 'quantity_diff': (data[item['cmdCode']]['quantity_a'] - net_weight),
                    # 'value_diff': (data[item['cmdCode']]['value_a'] - trade_value)
                })
            else:
                data[item[column_b]] = {
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

    def compile(self):
        pass

    def prepare(self, data):
        df = pd.DataFrame.from_dict(data, orient='index')
        df['value_diff'] = df['value_a'] - df['value_b']
        df['quantity_diff'] = df['quantity_a'] - df['quantity_b']
        df['quantity_diff'].round(2)
        df['value_diff'].round(2)
        df['quantity_pct'] = (df['quantity_diff'] / df['quantity_a']) * 100
        df['value_pct'] = (df['value_diff'] / df['value_a']) * 100
        df['quantity_pct'].round(2)
        df['value_pct'].round(2)
        df['value_diff_abs'] = abs(df['value_diff'])
        df['value_pct_abs'] = abs(df['value_pct'])
        return df