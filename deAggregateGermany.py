"""
Module for de-aggregating the Spain country data in home data

    Input: [text] country|date|MW_01|MW_02|...|MW_24
    Output: [text] date|company|homeId|KW_01|...|KW24|flatRate?|CustomerGroup
"""

from dumbo import MultiMapper, identitymapper, primary, secondary, JoinReducer
from collections import Counter
import random

__author__ = 'amd'

sep = '|'
sep_out = '|'
population = 500000

region = ["BER", "BRA", "BRE", "BAV", "SAX", "HES", "SAN", "BAD", "SAA", "WES"]
companies = ["EOn", "EOn", "EOn", "NERGIE", "NERGIE", "Amprion", "Amprion", "Amprion", "Evonik", "Evonik"]
groups = ["0", "0", "0", "0", "0", "1", "1", "1", "2", "2", "3", "3", "3", "3", "4"]
flatrates = ["Y", "Y", "Y", "N", "N", "N", "N", "N", "N", "N"]


def inputMapper(key, value):

    data = value.split(sep)

    country = data[0]

    if country != 'DE':
        return

    date = data[1]
    hours = Counter()

    for i in range(2, len(data)):
        try:
            hours[i-1] = int(data[i])
        except:
            continue

    yield date, hours


def customerMapper(key, value):

    data = value.split(sep)

    country = data[0]

    if country != 'DE':
        return

    date = data[1]
    hours = Counter()


    for n in range(0, population):
        for i in range(2, len(data)):
            try:
                hours[i-1] = random.randrange(0, int(data[i]))
            except:
                continue
        # Home Id
        reg = region[n % 10]
        i = 0
        n = str(n)
        while len(n) < 6:
            n = '0' + n

        yield date, (reg + n, hours)


class mergeByDateToRatio(JoinReducer):

    def primary(self, key, values):
        self.inputTotal = values.next()

    def secondary(self, key, values):

        customers = list(values)
        randTotal = Counter()
        ratio = Counter()

        for customer in customers:
            randTotal += customer[1]

        for hour in self.inputTotal:
            try:
                ratio[hour] = float(self.inputTotal[hour])/float(randTotal[hour])
            except:
                ratio[hour] = 0.0

        for customer in customers:
            for hour in customer[1]:
                customer[1][hour] = int(customer[1][hour] * ratio[hour] * 1000)

            yield customer[0], (key, customer[1])


def homeInfoReducer(key, values):

    homeId = str(key)
    company = random.choice(companies)
    group = random.choice(groups)
    flatrate = random.choice(flatrates)

    out = str(key)
    out += sep_out + random.choice(companies)
    out += sep_out + random.choice(groups)

    for date, hours in values:
        out = date + sep_out + company + sep_out + homeId
        for hour in range(1, 25):
            out += sep_out + str(hours[hour])
        out += sep_out + flatrate + sep_out + group
        yield out, ''



def runner(job):

    multimap = MultiMapper()

    opts = [("inputformat", "text"), ("outputformat", "text"), ]
    o1 = job.additer(inputMapper)
    o2 = job.additer(customerMapper, input=[job.root])
    multimap.add("pre1", primary(identitymapper))
    multimap.add("pre2", secondary(identitymapper))
    job.additer(multimap, mergeByDateToRatio, input=[o1, o2])
    job.additer(identitymapper, homeInfoReducer, opts=opts)


if __name__ == "__main__":
    from dumbo import main

    main(runner)
