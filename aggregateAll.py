"""
Module for aggregating home data in country data

    Input Spain: [text] homeId  date  company  power  KW_01  ...  KW24
    Input Germany: [text] date|company|homeId|KW_01|...|KW24|flatRate?|CustomerGroup
    Output: [text] country  date  MW_01  ...  MW24
"""

from dumbo import MultiMapper
from collections import Counter

__author__ = 'amd'

sep_DE = '|'
sep_ES = '\t'
sep_out = '\t'

def spainMapper(key, value):

    homeIdPos, datePos, companyPos, powerPos = range(0, 4)

    input = value.split(sep_ES)

    date = input[datePos]
    hours = Counter()

    for idx in range(4, 28):
        hours[idx - 3] = int(input[idx])

    yield (date, "ES"), hours


def germanyMapper(key, value):

    datePos, companyPos, homeIdPos = range(0, 3)
    flatratePos, groupPos = range(27, 29)

    input = value.split(sep_DE)

    date = input[datePos]
    hours = Counter()

    for idx in range(3, 27):
        hours[idx - 2] = int(input[idx])

    yield (date, "GE"), hours


def sumConsumptionReducer(key, values):

    date, country = key

    total = Counter()

    out = country + sep_out + date

    for value in values:
        total += value

    for idx in range(1, 25):
        out += sep_out + str(total[idx]/1000)

    yield out,''


def runner(job):

    multimap = MultiMapper()

    opts = [("inputformat", "text"), ("outputformat", "text"), ]
    multimap.add("ES_Mini", spainMapper)
    multimap.add("GE", germanyMapper)
    o1 = job.additer(multimap, sumConsumptionReducer, opts=opts)


if __name__ == "__main__":
    from dumbo import main

    main(runner)
