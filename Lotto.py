import csv
import random
lotto_db = [];

def read_lotto_file(depth=-1):
    input_file = csv.DictReader(open("Lotto.csv"))
    for row in input_file:
        if depth!=0:
            depth-=1
            row['numbers'] = [int(row['1']), int(row['2']), int(row['3']), int(row['4']), int(row['5']), int(row['6'])]
            row['sum'] = sum(row['numbers'])
            row['fullsum'] = row['sum']+int(row['Additional number'])
            row['average'] = row['sum'] / 6
            row['fullavg'] = row['fullsum'] / 7
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
        num_ranges[str(i)]['avg'] = sum(num_ranges[str(i)]['list'])/len(num_ranges[str(i)]['list'])
    return num_ranges

def dump_db(lotto_db):
    for row in lotto_db:
        #if (int(row['1'])>37 or int(row['2'])>37 or int(row['3'])>37 or int(row['4'])>37 or int(row['5'])>37 or int(row['6'])>37):
        print row['Game'],row['Date'],row['numbers'],row['Additional number'],row['sum']

def generate_results(res_num):
    random.seed()
    result = {}
    for j in range(1, res_num):
        result[str(j)] = {}
        result[str(j)]['list'] = []
        for i in range(1, 7):
            candidate = number_ranges(lotto_db)[str(i)]['list'][
                random.randint(1, len(number_ranges(lotto_db)[str(i)]['list']))]
            while candidate  in result[str(j)]['list']:
                candidate = number_ranges(lotto_db)[str(i)]['list'][
                    random.randint(1, len(number_ranges(lotto_db)[str(i)]['list']))]
            result[str(j)]['list'].append(candidate)
        result[str(j)]['list'] = sorted(result[str(j)]['list'])
        result[str(j)]['sum'] = sum(result[str(j)]['list'])
        result[str(j)]['avg'] = result[str(j)]['sum'] / len(result[str(j)]['list'])
        print result[str(j)]
    return result

def generate_probability_results(res_num):
    random.seed()
    result = {}
    plist = []
    for i in range(1,6):
        plist += [item for item in number_ranges(lotto_db)[str(i)]['list']]

    for j in range(1, res_num):
        result[str(j)] = {}
        result[str(j)]['list'] = []
        for i in range(1, 7):
            candidate = plist[random.randint(1, len(plist))]
            while candidate in result[str(j)]['list']:
                candidate = plist[random.randint(1, len(plist))]
            result[str(j)]['list'].append(candidate)
        result[str(j)]['list'] = sorted(result[str(j)]['list'])
        result[str(j)]['sum'] = sum(result[str(j)]['list'])
        result[str(j)]['avg'] = result[str(j)]['sum']/len(result[str(j)]['list'])
        print result[str(j)]
    return result

def sum_probability(lotto_db):
    prob_sum = {}
    for row in lotto_db:
        if prob_sum.get(str(row['sum'])):
            prob_sum[str(row['sum'])] += 1
        else:
            prob_sum[str(row['sum'])] = 1
    print sorted(prob_sum, key=prob_sum.get, reverse=True)
    return prob_sum

def normal_sum_dist():
    avg_sum = {}
    for n1 in range(1,33):
        for n2 in range(n1+1, 34):
            for n3 in range(n2+1, 35):
                for n4 in range(n3+1, 36):
                    for n5 in range(n4+1, 37):
                        for n6 in range(n5+1, 38):
                            if n1!=n2!=n3!=n4!=n5!=n6:
                                if avg_sum.get(str(n1+n2+n3+n4+n5+n6)):
                                    avg_sum[str(n1+n2+n3+n4+n5+n6)] += 1
                                else:
                                    avg_sum[str(n1+n2+n3+n4+n5+n6)] = 1
                                #print n1, n2, n3, n4, n5, n6, str(n1+n2+n3+n4+n5+n6)
    print sorted(avg_sum, key=avg_sum.get, reverse=True)

def two_following(numbers):
    for num in numbers:
        if num+1 in numbers or num-1 in numbers:
            return True
    return False

def in_last(numbers, lotto_db):
    for num in numbers:
        if num in lotto_db[0]['numbers']:
            return True
    return False

read_lotto_file()
print most_recent_number(lotto_db=lotto_db)
dump_db(lotto_db)
sum_probability(lotto_db)
#normal_sum_dist()
#print number_ranges(lotto_db)
#res = generate_results(100)
#pres = generate_probability_results(100)
#my_set = set()
#for i in range(1,7):
#    my_set.add(lotto_db[0][str(i)])

#for i in range(1,100):
#    print set(res[str(i)]['list']).intersection(set(pres[str(i)]['list']))
#normal_sum_dist()

#a = two_following([1,4,10,12,23,33])
#b = in_last([1,4,10,12,23,33], lotto_db)
count = 0
for row in lotto_db:
    if two_following(row['numbers']):
        print row['numbers']
        count+=1
print count
print len(lotto_db)





