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
        return data_out, data_in

    def compare_import(self, period=2019):
        data_in = self.comtrade.get_data(self.reporter_area, self.partner_area, 1, period)  # import
        time.sleep(1)
        data_out = self.comtrade.get_data(self.partner_area, self.reporter_area, 2, period)  # export
        return data_in, data_out

    def compare(self, data_a, data_b):
        pass
