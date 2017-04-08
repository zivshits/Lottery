import csv
import random
import numpy
lotto_db = []
numbers = {}

# Reads data from Israeli Lottery csv file, parses it and calculates sum and average
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

# Prints database
def dump_db(lotto_db):
    for row in lotto_db:
         # if (int(row['1'])>37 or int(row['2'])>37 or int(row['3'])>37 or int(row['4'])>37 or int(row['5'])>37 or int(row['6'])>37):
         print row['Game'], row['Date'], row['numbers'], row['Additional number'], row['sum'], row['fullsum']

# Returns a list of most recent numbers order
def most_recent_number(lotto_db):
    most_recent = {}
    for row in lotto_db:
        for i in range(1,7):
            if most_recent.get(row[str(i)]):
                most_recent[row[str(i)]] += 1
            else:
                most_recent[row[str(i)]] = 1

    return most_recent

# Returns a list of numbers per colomn
def number_ranges(lotto_db):
    num_ranges = {}
    num_ranges['Additional number'] = [int(row['Additional number']) for row in lotto_db]
    for i in range(1,7):
        num_ranges[str(i)] = {}
        num_ranges[str(i)]['min']=99
        num_ranges[str(i)]['max']=0
        num_ranges[str(i)]['list']=[]
        for row in lotto_db:
            num_ranges[str(i)]['min'] = min(num_ranges[str(i)]['min'], int(row[str(i)]))
            num_ranges[str(i)]['max'] = max(num_ranges[str(i)]['max'], int(row[str(i)]))
            num_ranges[str(i)]['list'].append(int(row[str(i)]))
        num_ranges[str(i)]['avg'] = sum(num_ranges[str(i)]['list'])/len(num_ranges[str(i)]['list'])
    return num_ranges


def generate_results(number_ranges):
    random.seed()
    result = {}
    result['list'] = []
    for i in range(1, 7):
        rrand = random.randint(0, len(number_ranges[str(i)]['list'])-1)
        candidate = number_ranges[str(i)]['list'][rrand]
        while candidate  in result['list']:
            candidate = number_ranges[str(i)]['list'][
                random.randint(0, len(number_ranges[str(i)]['list'])-1)]
        result['list'].append(candidate)
    result['list'] = sorted(result['list'])
    result['sum'] = sum(result['list'])
    result['avg'] = result['sum'] / len(result['list'])
    result['Additional number'] = number_ranges['Additional number'][random.randint(0, len(number_ranges['Additional number'])-1)]
    return result

def generate_probability_results(res_num):
    random.seed()
    result = {}
    plist = []
    for i in range(1,7):
        plist += [item for item in number_ranges(lotto_db)[str(i)]['list']]

    for j in range(1, res_num+1):
        result[str(j)] = {}
        result[str(j)]['list'] = []
        for i in range(1, 7):
            candidate = plist[random.randint(0, len(plist)-1)]
            while candidate in result[str(j)]['list']:
                candidate = plist[random.randint(0, len(plist)-1)]
            result[str(j)]['list'].append(candidate)
        result[str(j)]['list'] = sorted(result[str(j)]['list'])
        result[str(j)]['sum'] = sum(result[str(j)]['list'])
        result[str(j)]['avg'] = result[str(j)]['sum']/len(result[str(j)]['list'])
        print result[str(j)]
    return result

# Returns list of sum by probability (desc)
def sum_probability(lotto_db):
    prob_sum = {}
    for row in lotto_db:
        if prob_sum.get(str(row['sum'])):
            prob_sum[str(row['sum'])] += 1
        else:
            prob_sum[str(row['sum'])] = 1
    return prob_sum

# Returns normal distribution of sums
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

# Finds if there are 2 following numbers (1,2 or 11,12)
def two_following(numbers):
    for num in numbers:
        if num+1 in numbers or num-1 in numbers:
            return True
    return False


# Finds if numbers exists in the last lotto results
def in_last(numbers, lotto_db):
    count = 0
    for num in numbers:
        if num in lotto_db[0]['numbers']:
            count += 1
    return count

# Returns number of 2 following numbers in the lottery
def calculate_two_following(lotto_db):
    count = 0
    for row in lotto_db:
        if two_following(row['numbers']):
            print row['numbers']
            count += 1
    return count

# Returns number of appearence in the previous lotto results
def calculate_in_last(lotto_db):
    count = 0
    last = {}
    for row in lotto_db:
        for i in range(1, 7):
            if 'numbers' in last and int(row[str(i)]) in last['numbers']:
                count += 1
        last = row
    return count

#calculate less most recent number
def find_less_most_number_value():
    most_recent = most_recent_number(lotto_db=lotto_db)
    count=400
    for row in lotto_db:
        mid_most = 0
        for i in range(1,7):
            if mid_most < most_recent[row[str(i)]]:
                mid_most = most_recent[row[str(i)]]
        if count > mid_most:
            count = mid_most
    return count

def find_most_less_recent_number_index():
    most_recent = most_recent_number(lotto_db=lotto_db)
    count = 0
    for row in lotto_db:
        mid_most = 400
        for i in range(1, 7):
            if mid_most > most_recent[row[str(i)]]:
                mid_most = most_recent[row[str(i)]]
        if count < mid_most:
            count = mid_most
    return count

# Check if has most recent number in the list
def has_most_recent_number(numbers):
    count = 0
    less_most_recent_index = find_less_most_number_value()
    most_recent = most_recent_number(lotto_db=lotto_db)
    for number in numbers:
        if most_recent[str(number)] > less_most_recent_index:
            count += 1
    return count


# Preparations
read_lotto_file()

#print find_most_less_recent_number_index()

def find_number_of_most_numbers():
    slots = {'0':0, '1':0, '2':0, '3':0, '4':0, '5':0, '6':0}
    for row in lotto_db:
        slots[str(has_most_recent_number(row['numbers']))] += 1
    return slots

def number_pattern(lotto_db):
    numbers = {}
    for row in lotto_db:
        for i in range(1, 7):
            if row[str(i)] not in numbers:
                 numbers[row[str(i)]] = {'games':[], 'pattern':[]}
            numbers[row[str(i)]]['games'].append(row['Game'])
    for num in numbers:
        last_game = lotto_db[0]['Game']
        for game in numbers[num]['games']:
            numbers[num]['pattern'].append(int(last_game) - int(game))
            last_game = game
        numbers[num]['pattern_avg'] = numpy.mean(numbers[num]['pattern'])
        print num, numbers[num]
    return numbers


numbers = number_pattern(lotto_db)


final_results = []
ranges = number_ranges(lotto_db)
lotto_list = [row['numbers'] for row in lotto_db]
summary_list = sorted(sum_probability(lotto_db), key=sum_probability(lotto_db).get, reverse=True)
print "Main statistics"
print "==============================="
#print "Less most recent number index: "+str(find_less_most_number_value())
print "Ordered summary list: "+ str(summary_list)
#print "Number of most recent numbers: " + str(find_number_of_most_numbers())
print "Most recent numbers: " + str(sorted(most_recent_number(lotto_db), key=most_recent_number(lotto_db).get, reverse=True))
#print most_recent_number(lotto_db)
print "==============================="
print "Lotto results:"
while len(final_results) < 10:
    result = generate_results(ranges)
    if two_following(result['list']) and result['Additional number'] < 8:
        if in_last(result['list'], lotto_db) == 2:
            if has_most_recent_number(result['list']) == 4:
                if str(result['sum']) in summary_list[0:5]:
                    if result['list'] not in lotto_list and result not in final_results:
                        final_results.append(result)
                        print len(final_results), result