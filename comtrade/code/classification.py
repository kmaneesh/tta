from zipfile import ZipFile
import io
import csv

try:
    from config import *
except ImportError:
    from .config import *

DATA_SOURCE = str(ROOT_DIR)  + '/comtrade/code/classification.zip'


class ClassificationCode(object):
    def __init__(self):
        data_source = DATA_SOURCE
        self.records = []
        with ZipFile(data_source) as zf:
            with zf.open('classification.csv', 'r') as csvfile:
                reader = csv.DictReader(io.TextIOWrapper(csvfile, 'utf-8-sig'))
                for dct in map(dict, reader):
                    self.records.append(dct)
                    print(dct)

    def get_code(self, description):
        codes = []
        for record in self.records:
            if description.upper() in record['description'].upper():
                codes.append(record)
        return codes

    def get_description(self, code):
        description = None
        for record in self.records:
            if record['code'] == code:
                description = record['description']
                return description
        if not description:
            return 'Unknown'


if __name__ == '__main__':
    cc = ClassificationCode()
    print(cc.get_description('97101'))
