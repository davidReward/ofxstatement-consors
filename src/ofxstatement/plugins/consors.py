from ofxstatement.plugin import Plugin
from ofxstatement.parser import CsvStatementParser
from ofxstatement.statement import StatementLine
import csv
import sys


class ConsorsParser(CsvStatementParser):
    
    # 0 Buchung;
    # 1 Valuta 
    # 2 Sender / Empfänger
    # 3 IBAN / Konto-Nr.
    # 4 BIC / BLZ 
    # 5 Buchungstext 
    # 6 Verwendungszweck 
    # 7 Betrag in EUR

    mappings = {"date": 1, "amount": 7}
    date_format = "%Y-%m-%d"

    def split_records(self):
        return csv.reader(self.fin, delimiter=';')

    def parse_record(self, line):

        if self.cur_record == 1:
            self.statement.currency = line[7].strip('Betrag in ')
            return None

        # Remove dots (German decimal point handling)
        # 2.000,00 => 2000,00
        line[7] = line[7].replace('.', '')

        # Replace comma with dot (German decimal point handling)
        # 2000.00 => 2000.00
        line[7] = line[7].replace(',', '.')

        # fill statement line according to mappings
        sl = super(ConsorsParser, self).parse_record(line)

        sl.memo = line[2] + "; " + line[6] + "; " + line[5]

        # generate id for statement
        id_date = sl.date.strftime('%Y%m%d')

        # create a hash from date, memo, amount
        id_hash = str(hash(str(sl.date) + sl.memo + str(sl.amount)) % ((sys.maxsize + 1) * 2))

        # final id is constructed from date and hash (so hopefully this is unique)
        sl.id = id_date + id_hash

        return sl
 

class ConsorsPlugin(Plugin):

    def get_parser(self, filename):
        f = open(filename, "r", encoding='utf-8')
        parser = ConsorsParser(f)
        parser.statement.account_id = "Consorsbank-Konto"
        parser.statement.bank_id = "Consorsbank"
        return parser

