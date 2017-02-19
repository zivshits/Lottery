import csv
import random
lotto_db = [];

def read_lotto_file(depth=-1):
    input_file = csv.DictReader(open("Lotto.csv"))
    for row in input_file:
        if depth!=0:
            depth-=1
            lotto_db.append(row)

def most_recent_number(lotto_db):
    most_recent = {}
    for row in lotto_db:
        for i in range(1,6):
            if most_recent.get(row[str(i)]):
                most_recent[row[str(i)]] += 1
            else:
                most_recent[row[str(i)]] = 1

    return most_recent


def add_row_sum(lotto_db):
    for row in lotto_db:
        row['sum'] = int(row['1'])+int(row['2'])+int(row['3'])+int(row['4'])+int(row['5'])+int(row['6'])
        row['fullsum'] = row['sum']+int(row['Additional number'])

def add_row_average(lotto_db):
    for row in lotto_db:
        row['average'] = row['sum']/6
        row['fullavg'] = row['fullsum']/7

def number_ranges(lotto_db):
    num_ranges = {};
    for i in range(1,7):
        num_ranges[str(i)] = {};
        num_ranges[str(i)]['min']=99;
        num_ranges[str(i)]['max']=0;
        num_ranges[str(i)]['list']=[];
        for row in lotto_db:
            num_ranges[str(i)]['min'] = min(num_ranges[str(i)]['min'], int(row[str(i)]))
            num_ranges[str(i)]['max'] = max(num_ranges[str(i)]['max'], int(row[str(i)]))
            num_ranges[str(i)]['list'].append(int(row[str(i)]))
        num_ranges[str(i)]['avg'] = sum(num_ranges[str(i)]['list'])/float(len(num_ranges[str(i)]['list']))
    return num_ranges

def dump_db(lotto_db):
    for row in lotto_db:
        print row['Game'],row['Date'],row['1'],row['2'],row['3'],row['4'],row['5'],row['6'],row['Additional number']

def generate_results(res_num):
    random.seed()
    result = {}
    for j in range(1, res_num):
        result[str(j)] = []
        for i in range(1, 7):
            candidate = number_ranges(lotto_db)[str(i)]['list'][
                random.randint(1, len(number_ranges(lotto_db)[str(i)]['list']))]
            while candidate  in result[str(j)]:
                candidate = number_ranges(lotto_db)[str(i)]['list'][
                    random.randint(1, len(number_ranges(lotto_db)[str(i)]['list']))]
            result[str(j)].append(candidate)
        print sorted(result[str(j)])
    return result

def generate_probability_results(res_num):
    random.seed()
    result = {}
    plist = []
    for i in range(1,6):
        plist += [item for item in number_ranges(lotto_db)[str(i)]['list']]

    for j in range(1, res_num):
        result[str(j)] = []
        for i in range(1, 7):
            candidate = plist[random.randint(1, len(plist))]
            while candidate in result[str(j)]:
                candidate = plist[random.randint(1, len(plist))]
            result[str(j)].append(candidate)
        print sorted(result[str(j)])
    return result

read_lotto_file()
most_recent_number(lotto_db=lotto_db)
add_row_sum(lotto_db)
add_row_average(lotto_db)
dump_db(lotto_db)
print number_ranges(lotto_db)
res = generate_results(100)
pres = generate_probability_results(100)





