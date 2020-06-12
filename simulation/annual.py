try:
    from config import *
except ImportError:
    from .config import *

import time

from comtrade.api.public import PublicApi


class Annual(object):
    def __init__(self):
        self.comtrade = PublicApi()

    def set_source_destination(self, source, destination):
        self.reporter_area = source
        self.partner_area = destination

    def source_data_available(self, period=2019):
        return self.comtrade.data_available(reporter_area=self.reporter_area, period=period)

    def destination_data_available(self, period=2019):
        return self.comtrade.data_available(reporter_area=self.partner_area, period=period)

    def compare_export(self, period=2019):
        data_out = self.comtrade.get_data(self.reporter_area, self.partner_area, 2, period)  # export
        time.sleep(1)
        data_in = self.comtrade.get_data(self.partner_area, self.reporter_area, 1, period)  # import
        return self.compare(data_out, data_in)

    def compare_import(self, period=2019):
        data_in = self.comtrade.get_data(self.reporter_area, self.partner_area, 1, period)  # import
        time.sleep(1)
        data_out = self.comtrade.get_data(self.partner_area, self.reporter_area, 2, period)  # export
        return self.compare(data_in, data_out)

    def compare(self, data_a, data_b):
        data = {}
        for item in data_a['dataset']:
            if item['cmdCode'] in data:
                print("Duplicate cmdCode found")
            else:
                data[item['cmdCode']] = {
                    'desc': item['cmdDescE'],
                    'quantity_a': item['NetWeight'],
                    'quantity_desc_a': item['qtDesc'],
                    'value_a': item['TradeValue'],
                    'quantity_b': 0,
                    'quantity_desc_b': item['qtDesc'],
                    'value_b': 0
                }

        for item in data_b['dataset']:
            if item['cmdCode'] in data:
                data[item['cmdCode']].update({
                    'quantity_b': item['NetWeight'],
                    'quantity_desc_b': item['qtDesc'],
                    'value_b': item['TradeValue']
                })
            else:
                data[item['cmdCode']] = {
                    'desc': item['cmdDescE'],
                    'quantity_a': 0,
                    'quantity_desc_a': item['qtDesc'],
                    'value_a': 0,
                    'quantity_b': item['NetWeight'],
                    'quantity_desc_b': item['qtDesc'],
                    'value_b': item['TradeValue']
                }
        return data

