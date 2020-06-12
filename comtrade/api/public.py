try:
    from config import *
except ImportError:
    from .config import *

import requests

class PublicApi(object):

    def __init__(self):
        self.reporter_area = 699
        self.partner_area = 344
        self.frequency = 'A'
        self.max_records = '100000'
        self.classification = 'HS'
        self.period = 2019
        self.aggregation = 'AG6'


    def data_available(self, reporter_area, period = 2019, classification = 'HS', frequency = 'A'):
        url = "http://comtrade.un.org/api/refs/da/view"
        params = {'r': reporter_area, 'ps': period, 'px': classification, 'freq': frequency}
        r = requests.get(url=url, params=params)
        return r.json()


    def get_data(self, reporter_area, partner_area, regime=1, period=2019, classification='HS', frequency = 'A', aggregation='AG6'):
        url = "http://comtrade.un.org/api/get"
        params = {
            'r': reporter_area,
            'p': partner_area,
            'rg': regime,
            'ps': period,
            'px': classification,
            'cc': aggregation,
            'freq': frequency,
            'max': self.max_records
        }
        r = requests.get(url=url, params=params)
        return r.json()