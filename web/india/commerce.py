try:
    from config import *
except ImportError:
    from .config import *

import requests
from lxml.html import fromstring

class Commerce(object):
    def __init__(self):
        self.headers = {
            'Host': 'commerce-app.gov.in',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': '*/*'
        }
        pass

    def get_calendar_year_data(self, country, year, hs, export =0):
        data = []
        for month in range(1, 13):
            records = self.get_month_data(country, year, month, hs, export)
            data.append(records)
        return self.sum_data(data)

    def get_year_data(self, country, year, hs, export=0):
        if export:
            self.url = "https://commerce-app.gov.in/eidb/ecntcom.asp"
        else:
            self.url = "https://commerce-app.gov.in/eidb/icomxcntq.asp"
        data = {
            'yy1': year,
            'cntcode': country,
            'hslevel': hs,
            'sort': 0,
            'radioDAll': 1,
            'radiousd': 1
        }
        r = requests.post(url=self.url, data=data, headers=self.headers, verify=False)
        return self.parse_data(r.text)

    def get_month_data(self, country, year, month, hs, export=0):
        if export:
            self.url = "https://commerce-app.gov.in/meidb/cntcom.asp?ie=e"
        else:
            self.url = "https://commerce-app.gov.in/meidb/cntcom.asp?ie=i"
        data = {
            'radioFY': 1,
            'Mm1': month,
            'yy1': year,
            'cntcode': country,
            'hslevel': hs,
            'sort': 0,
            'radioDAll': 1,
            'radiousd': 1
        }
        r = requests.post(url=self.url, data=data, headers=self.headers, verify=False)
        return self.parse_data(r.text)

    def parse_data(self, data):
        output = {}
        root = fromstring(data)
        table = root.xpath('/html/body/table')[0]
        cnt = 0
        for row in table.xpath('.//tr'):
            item = {}
            if cnt == 0:
                pass
            else:
                item['hscode'] = self.clean_text(row.xpath('.//td[2]//font//text()'))
                item['description'] = self.clean_text(row.xpath('.//td[3]//font//text()'))
                item['pvalue'] = 0 if self.clean_text(row.xpath('.//td[4]//font//text()')) == '' else float(self.clean_text(row.xpath('.//td[4]//font//text()')).replace(',',''))
                item['value'] = 0 if self.clean_text(row.xpath('.//td[5]//font//text()')) == '' else float(self.clean_text(row.xpath('.//td[5]//font//text()')).replace(',',''))
                item['growth'] = 0 if self.clean_text(row.xpath('.//td[6]//font//text()')) == '' else float(self.clean_text(row.xpath('.//td[6]//font//text()')).replace(',',''))
                output[item['hscode']] = item
            cnt = cnt + 1
        return output

    def sum_data(self, data):
        output = {}
        for records in data:
            for key, record in records.items():

                if record['hscode'] in output:
                    output[record['hscode']]['pvalue'] = output[record['hscode']]['pvalue'] + record['pvalue']
                    output[record['hscode']]['value'] = output[record['hscode']]['value'] + record['value']
                else:
                    output[record['hscode']] = {}
                    output[record['hscode']]['hscode'] = record['hscode']
                    output[record['hscode']]['description'] = record['description']
                    output[record['hscode']]['pvalue'] = record['pvalue']
                    output[record['hscode']]['value'] = record['value']
        return output

    def clean_text(self, text):
        text = ' '.join(text)
        return text.strip()

    def get_country_code(self, country_name):

        country_codes = [
            {'code': '1', 'text': 'AFGHANISTAN TIS'},
            {'code': '3', 'text': 'ALBANIA'},
            {'code': '5', 'text': 'ALGERIA'},
            {'code': '7', 'text': 'AMERI SAMOA'},
            {'code': '9', 'text': 'ANDORRA'},
            {'code': '11', 'text': 'ANGOLA'},
            {'code': '12', 'text': 'ANGUILLA'},
            {'code': '14', 'text': 'ANTARTICA'},
            {'code': '13', 'text': 'ANTIGUA'},
            {'code': '15', 'text': 'ARGENTINA'},
            {'code': '16', 'text': 'ARMENIA'},
            {'code': '20', 'text': 'ARUBA'},
            {'code': '17', 'text': 'AUSTRALIA'},
            {'code': '19', 'text': 'AUSTRIA'},
            {'code': '21', 'text': 'AZERBAIJAN'},
            {'code': '23', 'text': 'BAHAMAS'},
            {'code': '25', 'text': 'BAHARAIN IS'},
            {'code': '27', 'text': 'BANGLADESH PR'},
            {'code': '29', 'text': 'BARBADOS'},
            {'code': '55', 'text': 'BELARUS'},
            {'code': '33', 'text': 'BELGIUM'},
            {'code': '31', 'text': 'BELIZE'},
            {'code': '35', 'text': 'BENIN'},
            {'code': '37', 'text': 'BERMUDA'},
            {'code': '38', 'text': 'BHUTAN'},
            {'code': '39', 'text': 'BOLIVIA'},
            {'code': '40', 'text': 'BOSNIA-HRZGOVIN'},
            {'code': '41', 'text': 'BOTSWANA'},
            {'code': '45', 'text': 'BR VIRGN IS'},
            {'code': '43', 'text': 'BRAZIL'},
            {'code': '47', 'text': 'BRUNEI'},
            {'code': '49', 'text': 'BULGARIA'},
            {'code': '50', 'text': 'BURKINA FASO'},
            {'code': '53', 'text': 'BURUNDI'},
            {'code': '67', 'text': 'C AFRI REP'},
            {'code': '56', 'text': 'CAMBODIA'},
            {'code': '57', 'text': 'CAMEROON'},
            {'code': '59', 'text': 'CANADA'},
            {'code': '61', 'text': 'CANARY IS'},
            {'code': '63', 'text': 'CAPE VERDE IS'},
            {'code': '65', 'text': 'CAYMAN IS'},
            {'code': '69', 'text': 'CHAD'},
            {'code': '71', 'text': 'CHANNEL IS'},
            {'code': '73', 'text': 'CHILE'},
            {'code': '77', 'text': 'CHINA P RP'},
            {'code': '79', 'text': 'CHRISTMAS IS.'},
            {'code': '81', 'text': 'COCOS IS'},
            {'code': '83', 'text': 'COLOMBIA'},
            {'code': '85', 'text': 'COMOROS'},
            {'code': '459', 'text': 'CONGO D. REP.'},
            {'code': '87', 'text': 'CONGO P REP'},
            {'code': '89', 'text': 'COOK IS'},
            {'code': '91', 'text': 'COSTA RICA'},
            {'code': '199', 'text': 'COTE D IVOIRE'},
            {'code': '92', 'text': 'CROATIA'},
            {'code': '93', 'text': 'CUBA'},
            {'code': '276', 'text': 'CURACAO'},
            {'code': '95', 'text': 'CYPRUS'},
            {'code': '98', 'text': 'CZECH REPUBLIC'},
            {'code': '101', 'text': 'DENMARK'},
            {'code': '102', 'text': 'DJIBOUTI'},
            {'code': '103', 'text': 'DOMINIC REP'},
            {'code': '105', 'text': 'DOMINICA'},
            {'code': '109', 'text': 'ECUADOR'},
            {'code': '111', 'text': 'EGYPT A RP'},
            {'code': '113', 'text': 'EL SALVADOR'},
            {'code': '117', 'text': 'EQUTL GUINEA'},
            {'code': '116', 'text': 'ERITREA'},
            {'code': '114', 'text': 'ESTONIA'},
            {'code': '115', 'text': 'ETHIOPIA'},
            {'code': '123', 'text': 'FALKLAND IS'},
            {'code': '121', 'text': 'FAROE IS.'},
            {'code': '127', 'text': 'FIJI IS'},
            {'code': '125', 'text': 'FINLAND'},
            {'code': '131', 'text': 'FR GUIANA'},
            {'code': '133', 'text': 'FR POLYNESIA'},
            {'code': '135', 'text': 'FR S ANT TR'},
            {'code': '129', 'text': 'FRANCE'},
            {'code': '141', 'text': 'GABON'},
            {'code': '143', 'text': 'GAMBIA'},
            {'code': '145', 'text': 'GEORGIA'},
            {'code': '147', 'text': 'GERMANY'},
            {'code': '149', 'text': 'GHANA'},
            {'code': '151', 'text': 'GIBRALTAR'},
            {'code': '155', 'text': 'GREECE'},
            {'code': '157', 'text': 'GREENLAND'},
            {'code': '159', 'text': 'GRENADA'},
            {'code': '161', 'text': 'GUADELOUPE'},
            {'code': '163', 'text': 'GUAM'},
            {'code': '165', 'text': 'GUATEMALA'},
            {'code': '124', 'text': 'GUERNSEY'},
            {'code': '167', 'text': 'GUINEA'},
            {'code': '169', 'text': 'GUINEA BISSAU'},
            {'code': '171', 'text': 'GUYANA'},
            {'code': '175', 'text': 'HAITI'},
            {'code': '176', 'text': 'HEARD MACDONALD'},
            {'code': '177', 'text': 'HONDURAS'},
            {'code': '179', 'text': 'HONG KONG'},
            {'code': '181', 'text': 'HUNGARY'},
            {'code': '185', 'text': 'ICELAND'},
            {'code': '187', 'text': 'INDONESIA'},
            {'code': '2', 'text': 'INSTALLATIONS IN INTERNATIONAL WATERS'},
            {'code': '189', 'text': 'IRAN'},
            {'code': '191', 'text': 'IRAQ'},
            {'code': '193', 'text': 'IRELAND'},
            {'code': '195', 'text': 'ISRAEL'},
            {'code': '197', 'text': 'ITALY'},
            {'code': '203', 'text': 'JAMAICA'},
            {'code': '205', 'text': 'JAPAN'},
            {'code': '122', 'text': 'JERSEY '},
            {'code': '207', 'text': 'JORDAN'},
            {'code': '212', 'text': 'KAZAKHSTAN'},
            {'code': '213', 'text': 'KENYA'},
            {'code': '214', 'text': 'KIRIBATI REP'},
            {'code': '215', 'text': 'KOREA DP RP'},
            {'code': '217', 'text': 'KOREA RP'},
            {'code': '219', 'text': 'KUWAIT'},
            {'code': '216', 'text': 'KYRGHYZSTAN'},
            {'code': '223', 'text': 'LAO PD RP'},
            {'code': '224', 'text': 'LATVIA'},
            {'code': '225', 'text': 'LEBANON'},
            {'code': '227', 'text': 'LESOTHO'},
            {'code': '229', 'text': 'LIBERIA'},
            {'code': '231', 'text': 'LIBYA'},
            {'code': '233', 'text': 'LIECHTENSTEIN'},
            {'code': '234', 'text': 'LITHUANIA'},
            {'code': '235', 'text': 'LUXEMBOURG'},
            {'code': '239', 'text': 'MACAO'},
            {'code': '240', 'text': 'MACEDONIA'},
            {'code': '241', 'text': 'MADAGASCAR'},
            {'code': '243', 'text': 'MALAWI'},
            {'code': '245', 'text': 'MALAYSIA'},
            {'code': '247', 'text': 'MALDIVES'},
            {'code': '249', 'text': 'MALI'},
            {'code': '251', 'text': 'MALTA'},
            {'code': '252', 'text': 'MARSHALL ISLAND'},
            {'code': '253', 'text': 'MARTINIQUE'},
            {'code': '255', 'text': 'MAURITANIA'},
            {'code': '257', 'text': 'MAURITIUS'},
            {'code': '34', 'text': 'MAYOTTE'},
            {'code': '259', 'text': 'MEXICO'},
            {'code': '256', 'text': 'MICRONESIA'},
            {'code': '260', 'text': 'MOLDOVA'},
            {'code': '262', 'text': 'MONACO'},
            {'code': '261', 'text': 'MONGOLIA'},
            {'code': '356', 'text': 'MONTENEGRO'},
            {'code': '263', 'text': 'MONTSERRAT'},
            {'code': '265', 'text': 'MOROCCO'},
            {'code': '267', 'text': 'MOZAMBIQUE'},
            {'code': '258', 'text': 'MYANMAR'},
            {'code': '294', 'text': 'N. MARIANA IS.'},
            {'code': '269', 'text': 'NAMIBIA'},
            {'code': '271', 'text': 'NAURU RP'},
            {'code': '273', 'text': 'NEPAL'},
            {'code': '275', 'text': 'NETHERLAND'},
            {'code': '277', 'text': 'NETHERLANDANTIL'},
            {'code': '279', 'text': 'NEUTRAL ZONE'},
            {'code': '281', 'text': 'NEW CALEDONIA'},
            {'code': '285', 'text': 'NEW ZEALAND'},
            {'code': '287', 'text': 'NICARAGUA'},
            {'code': '289', 'text': 'NIGER'},
            {'code': '291', 'text': 'NIGERIA'},
            {'code': '293', 'text': 'NIUE IS'},
            {'code': '295', 'text': 'NORFOLK IS'},
            {'code': '297', 'text': 'NORWAY'},
            {'code': '301', 'text': 'OMAN'},
            {'code': '307', 'text': 'PACIFIC IS'},
            {'code': '309', 'text': 'PAKISTAN IR'},
            {'code': '310', 'text': 'PALAU'},
            {'code': '313', 'text': 'PANAMA C Z'},
            {'code': '311', 'text': 'PANAMA REPUBLIC'},
            {'code': '315', 'text': 'PAPUA N GNA'},
            {'code': '317', 'text': 'PARAGUAY'},
            {'code': '319', 'text': 'PERU'},
            {'code': '0', 'text': 'Petroleum Products'},
            {'code': '323', 'text': 'PHILIPPINES'},
            {'code': '321', 'text': 'PITCAIRN IS.'},
            {'code': '325', 'text': 'POLAND'},
            {'code': '327', 'text': 'PORTUGAL'},
            {'code': '331', 'text': 'PUERTO RICO'},
            {'code': '335', 'text': 'QATAR'},
            {'code': '339', 'text': 'REUNION'},
            {'code': '343', 'text': 'ROMANIA'},
            {'code': '344', 'text': 'RUSSIA'},
            {'code': '345', 'text': 'RWANDA'},
            {'code': '347', 'text': 'SAHARWI A.DM RP'},
            {'code': '447', 'text': 'SAMOA'},
            {'code': '346', 'text': 'SAN MARINO'},
            {'code': '349', 'text': 'SAO TOME'},
            {'code': '351', 'text': 'SAUDI ARAB'},
            {'code': '353', 'text': 'SENEGAL'},
            {'code': '352', 'text': 'SERBIA'},
            {'code': '355', 'text': 'SEYCHELLES'},
            {'code': '357', 'text': 'SIERRA LEONE'},
            {'code': '359', 'text': 'SINGAPORE'},
            {'code': '278', 'text': 'SINT MAARTEN (DUTCH PART)'},
            {'code': '358', 'text': 'SLOVAK REP'},
            {'code': '360', 'text': 'SLOVENIA'},
            {'code': '361', 'text': 'SOLOMON IS'},
            {'code': '363', 'text': 'SOMALIA'},
            {'code': '365', 'text': 'SOUTH AFRICA'},
            {'code': '382', 'text': 'SOUTH SUDAN '},
            {'code': '367', 'text': 'SPAIN'},
            {'code': '369', 'text': 'SRI LANKA DSR'},
            {'code': '371', 'text': 'ST HELENA'},
            {'code': '373', 'text': 'ST KITT N A'},
            {'code': '375', 'text': 'ST LUCIA'},
            {'code': '377', 'text': 'ST PIERRE'},
            {'code': '379', 'text': 'ST VINCENT'},
            {'code': '196', 'text': 'STATE OF PALEST'},
            {'code': '381', 'text': 'SUDAN'},
            {'code': '383', 'text': 'SURINAME'},
            {'code': '6', 'text': 'SVALLBARD AND J'},
            {'code': '385', 'text': 'SWAZILAND'},
            {'code': '387', 'text': 'SWEDEN'},
            {'code': '389', 'text': 'SWITZERLAND'},
            {'code': '391', 'text': 'SYRIA'},
            {'code': '75', 'text': 'TAIWAN'},
            {'code': '393', 'text': 'TAJIKISTAN'},
            {'code': '395', 'text': 'TANZANIA REP'},
            {'code': '397', 'text': 'THAILAND'},
            {'code': '329', 'text': 'TIMOR LESTE'},
            {'code': '399', 'text': 'TOGO'},
            {'code': '401', 'text': 'TOKELAU IS'},
            {'code': '403', 'text': 'TONGA'},
            {'code': '999', 'text': 'Trade to Unspecified Countries'},
            {'code': '405', 'text': 'TRINIDAD'},
            {'code': '407', 'text': 'TUNISIA'},
            {'code': '409', 'text': 'TURKEY'},
            {'code': '410', 'text': 'TURKMENISTAN'},
            {'code': '411', 'text': 'TURKS C IS'},
            {'code': '413', 'text': 'TUVALU'},
            {'code': '419', 'text': 'U ARAB EMTS'},
            {'code': '421', 'text': 'U K'},
            {'code': '423', 'text': 'U S A'},
            {'code': '417', 'text': 'UGANDA'},
            {'code': '422', 'text': 'UKRAINE'},
            {'code': '354', 'text': 'UNION OF SERBIA & MONTENEGRO'},
            {'code': '599', 'text': 'UNSPECIFIED'},
            {'code': '427', 'text': 'URUGUAY'},
            {'code': '424', 'text': 'US MINOR OUTLYING ISLANDS '},
            {'code': '430', 'text': 'UZBEKISTAN'},
            {'code': '431', 'text': 'VANUATU REP'},
            {'code': '198', 'text': 'VATICAN CITY'},
            {'code': '433', 'text': 'VENEZUELA'},
            {'code': '437', 'text': 'VIETNAM SOC REP'},
            {'code': '439', 'text': 'VIRGIN IS US'},
            {'code': '443', 'text': 'WALLIS F IS'},
            {'code': '453', 'text': 'YEMEN REPUBLC'},
            {'code': '461', 'text': 'ZAMBIA'},
            {'code': '463', 'text': 'ZIMBABWE'}]

        code = None
        for record in country_codes:
            if record['text'].upper() == country_name.upper():
                code = record['code']
                return code
        if not code:
            return '999'
