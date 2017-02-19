import csv

input_file = csv.DictReader(open("Lotto.csv"))
lotto_db = [row for row in input_file]



def most_recent_number(lotto_db):
    most_recent = {}
    for row in lotto_db:
        for i in range(1,6):
            if most_recent.get(row[str(i)]):
                most_recent[row[str(i)]] += 1
            else:
                most_recent[row[str(i)]] = 1

    print most_recent
    return most_recent


def add_row_sum(lotto_db):
    for row in lotto_db:
        row['sum'] = int(row['1'])+int(row['2'])+int(row['3'])+int(row['4'])+int(row['5'])+int(row['6'])

def add_row_average(lotto_db):
    for row in lotto_db:
        row['average'] = row['sum']/6

def dump_db(lotto_db):
    for row in lotto_db:
        print row['Game'],row['Date'],row['1'],row['2'],row['3'],row['4'],row['5'],row['6'],row['Additional number']

most_recent_number(lotto_db=lotto_db)
add_row_sum(lotto_db)
add_row_average(lotto_db)
dump_db(lotto_db)




