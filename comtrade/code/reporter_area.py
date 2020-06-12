from zipfile import ZipFile
import io
import csv

try:
    from config import *
except ImportError:
    from .config import *

DATA_SOURCE = str(ROOT_DIR)  + '/comtrade/code/reporter_area.zip'


class ReporterArea(object):
    def __init__(self):
        data_source = DATA_SOURCE
        self.records = []
        with ZipFile(data_source) as zf:
            with zf.open('reporter_area.csv', 'r') as csvfile:
                reader = csv.DictReader(io.TextIOWrapper(csvfile, 'utf-8-sig'))
                for dct in map(dict, reader):
                    self.records.append(dct)

    def get_ids(self, area_name):
        ids =[]
        for record in self.records:
            if area_name.upper() in record['text'].upper():
                ids.append(record)
        return ids

if __name__ == '__main__':
    ra = ReporterArea()
    print(ra.get_ids('INDIA'))
