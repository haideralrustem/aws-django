import pdb
import django
import os
from datetime import datetime, time, timedelta
import my_functions as mf

import openpyxl
import re
import dateutil.parser
from openpyxl.cell import cell


# print(django.get_version())
nt = '\n\t'
nl = '\n'


s = '05:35'


rows = [

    {'date': datetime.timedelta(days=2, seconds=25200), 'close': 40.1, 'loss': 70, 'profit': 0.9},
    {'date': datetime.timedelta(days=2, seconds=28800), 'close': 45, 'loss': 33, 'profit': 31},
    {'date': datetime.timedelta(days=2, seconds=32400), 'close': 8, 'loss': 'ui', 'profit': 5},
    {'date': datetime.timedelta(days=2, seconds=36000), 'close': 'jkrowling', 'loss': None, 'profit': 30},
    {'date': datetime.timedelta(days=2, seconds=39600), 'close': 'jkrowling', 'loss': datetime.timedelta(days=2, seconds=28800), 'profit': 8},
    {'date': datetime.timedelta(days=2, seconds=43200), 'close': 'jkrowling', 'loss': 49, 'profit': 10},
    {'date': datetime.timedelta(days=2, seconds=46800), 'close': 62, 'loss': datetime.datetime(2009, 7, 6, 0, 0), 'profit': 40}    

]
nrows = mf.serialize_data(rows)

print(nrows)