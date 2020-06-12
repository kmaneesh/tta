from zipfile import ZipFile
import io
import csv

try:
    from config import *
except ImportError:
    from .config import *

DATA_SOURCE = str(ROOT_DIR)  + '/comtrade/code/country.zip'


class CountryCode(object):
    def __init__(self):
        data_source = DATA_SOURCE
        self.records = []
        with ZipFile(data_source) as zf:
            with zf.open('country_code.csv', 'r') as csvfile:
                reader = csv.DictReader(io.TextIOWrapper(csvfile, 'utf-8'))
                for dct in map(dict, reader):
                    self.records.append(dct)

    def get_country_iso2(self, iso2):
        country_name = None
        for record in self.records:
            if record['iso2'] == iso2:
                country_name = record['country_name']
                return country_name
        if not country_name:
            return 'Unknown'

    def get_country_iso3(self, iso3):
        country_name = None
        for record in self.records:
            if record['iso3'] == iso3:
                country_name = record['country_name']
                return country_name
        if not country_name:
            return 'Unknown'

    def get_country(self, country_name):
        country_name = None
        for record in self.records:
            if record['country_name'].upper() == country_name.upper():
                country_name = record['country_name']
                return country_name
        if not country_name:
            return 'Unknown'

    def get_iso2_country(self, country_name):
        iso2 = None
        for record in self.records:
            if record['country_name'].upper() == country_name.upper():
                iso2 = record['iso2']
                return iso2
        if not iso2:
            return 'UN'

    def get_iso3_country(self, country_name):
        iso3 = None
        for record in self.records:
            if record['country_name'].upper() == country_name.upper():
                iso3 = record['iso3']
                return iso3
        if not iso3:
            return 'UNK'


if __name__ == '__main__':
    cc = CountryCode()
    print(cc.get_iso3_country('INDIA'))
