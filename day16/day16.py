import sys
import re
from functools import lru_cache, reduce

def parse_file(filename):
    f = open(filename)
    fields, my_ticket, other_tickets = f.read().split('\n\n')
    return fields, my_ticket, other_tickets

def parse_ticket(line):
    return [int(number) for number in line.split(',')]

def parse_tickets(tickets):
    lines = tickets.split('\n')
    return [parse_ticket(line) for line in lines[1:]]

INTERVAL_PATTERN = re.compile(r'(\d+)-(\d+)')
def get_all_intervals_from_fields(fields):
    return frozenset({(int(i_min), int(i_max)) for i_min, i_max in INTERVAL_PATTERN.findall(fields)})

# eg:
# departure track: 49-909 or 924-965
FIELD_PATTERN = re.compile(r'([a-z ]+): (\d+)-(\d+) or (\d+)-(\d+)')
def fields_interval_mapping(fields):
    mapping = {}
    for name, min1, max1, min2, max2 in FIELD_PATTERN.findall(fields):
        mapping[(int(min1), int(max1))] = name
        mapping[(int(min2), int(max2))] = name
    return mapping

NUMBER_PATTERN = re.compile(r'\d+')
def numbers_from_tickets(tickets):
    return (int(number) for number in NUMBER_PATTERN.findall(tickets))

@lru_cache(maxsize=None)
def is_valid(number, intervals):
    return len(valid_intervals_for_number(number, intervals)) > 0

@lru_cache(maxsize=None)
def valid_intervals_for_number(number, intervals):
    return {interval for interval in intervals if is_valid_for_interval(number, interval)}

def get_valid_fields_for_number_checker(fields, intervals):
    fields_by_interval = fields_interval_mapping(fields)

    def valid_fields(number):
        valid_intervals = valid_intervals_for_number(number, intervals)
        return {fields_by_interval[interval] for interval in valid_intervals}

    def memoize(f):
        memo = {}
        def helper(x):
            if x not in memo:            
                memo[x] = f(x)
            return memo[x]
        return helper
    
    return memoize(valid_fields)

@lru_cache(maxsize=None)
def is_valid_for_interval(number, interval):
    i_min, i_max = interval
    return number >= i_min and number <= i_max

def is_valid_ticket(ticket, intervals):
    return all((is_valid(number, intervals) for number in ticket))

# change the input here
file = './day16/input'
fields, my_ticket, other_tickets = parse_file(file)
intervals = get_all_intervals_from_fields(fields)

# Part 1
invalid_numbers = [number for number in numbers_from_tickets(other_tickets) if not is_valid(number, intervals)]
print(sum(invalid_numbers))

# Part 2
valid_tickets = [ticket for ticket in parse_tickets(other_tickets) if is_valid_ticket(ticket, intervals)]
field_names_for_number = get_valid_fields_for_number_checker(fields, intervals)

nb_of_fields = len(valid_tickets[0])
possible_fields_in_order = []

for i in range(nb_of_fields):
    possible_field_names = [field_names_for_number(ticket[i]) for ticket in valid_tickets]
    possible_fields_in_order.append(reduce(lambda a, b : a & b, possible_field_names))

min_length = min((len(candidates) for candidates in possible_fields_in_order))
assert(min_length == 1) # this algorithm will not work unless some fields have only one candidate

assigned_field_names = {}
max_length = max((len(candidates) for candidates in possible_fields_in_order))
while max_length > 0:
    # find columns with just one possible field
    assigned_field_names.update({candidates.pop(): index for index, candidates in enumerate(possible_fields_in_order) if len(candidates) == 1})
    # remove it from other columns
    for candidates in possible_fields_in_order:
        candidates -= set(assigned_field_names.keys())
    max_length = max((len(candidates) for candidates in possible_fields_in_order))

departure_fields_positions = [position for (name, position) in assigned_field_names.items() if name.find('departure') == 0]
my_ticket_values = parse_tickets(my_ticket)[0]
departure_fields_values = [my_ticket_values[pos] for pos in departure_fields_positions]
print(reduce(lambda a, b: a * b, departure_fields_values, 1))