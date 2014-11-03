"""
Module for de-aggregating the Spain country data in home data

    Input: [text] country|date|MW_01|MW_02|...|MW_24
    Output: [text] homeId  date  company  power  KW_01  ...  KW24
"""


from dumbo import MultiMapper, identitymapper, primary, secondary, JoinReducer
from collections import Counter
import random


__author__ = 'amd'

sep = '|'
sep_out = '\t'

# Number of total homes - Number of empty homes
population = 18217300 - 5500000

companies = ["Iberdrola", "Endesa", "Fenosa", "Eon", "Enerco", "Electra", "Nexus", "Hidroelectrica", "Iberdrola", "Endesa", "Fenosa", "Iberdrola", "Endesa", "Fenosa"]
powers = ["1.150 Kw", "1725 Kw", "2.300 Kw", "3.450 Kw",  "2.300 Kw", "3.450 Kw",  "2.300 Kw", "3.450 Kw", "4.600 Kw", "5.750 Kw"]


def inputMapper(key, value):

    data = value.split(sep)

    country = data[0]

    if country != 'ES':
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

    if country != 'ES':
        return

    date = data[1]
    hours = Counter()

    for n in range(0, population):
        for i in range(2, len(data)):
            try:
                hours[i-1] = random.randrange(0, int(data[i]))
            except:
                continue

        yield date, (n, hours)


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
    power = random.choice(powers)
    out = str(key)
    out += sep_out + random.choice(companies)
    out += sep_out + random.choice(powers)

    for date, hours in values:
        out = homeId + sep_out + date + sep_out + company + sep_out + power
        for hour in range(1, 25):
            out += sep_out + str(hours[hour])
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
