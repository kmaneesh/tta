try:
    from config import *
except ImportError:
    from .config import *

import requests
import time

class Api(object):

    def __init__(self):
        # Sensible default
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


    def get_data(self, reporter_area, partner_area, regime=1, period=2019, aggregation='AG6', frequency = 'A', classification='HS'):
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
        print(params) # debug
        r = requests.get(url=url, params=params)
        return r.json()

    def get_month_data(self, reporter_area, partner_area, regime=1, period=2019, aggregation='TOTAL', frequency = 'M', classification='HS'):
        data = {}
        url = "http://comtrade.un.org/api/get"
        months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
        for month in months:
            time.sleep(1)
            year_month = str(period) + month
            params = {
                'r': reporter_area,
                'p': partner_area,
                'rg': regime,
                'ps': year_month,
                'px': classification,
                'cc': aggregation,
                'freq': frequency,
                'max': self.max_records
            }
            print(params) # debug
            r = requests.get(url=url, params=params)
            records = r.json()
            if len(records['dataset']):
                data[year_month] = records['dataset'][0]['TradeValue']

            else:
                data[year_month] = 0
        return data