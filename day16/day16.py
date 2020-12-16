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
    memo = {}
    def valid_fields(number):
        if number not in memo:
            valid_intervals = valid_intervals_for_number(number, intervals)
            memo[number] = {fields_by_interval[interval] for interval in valid_intervals}
        return memo[number]
    return valid_fields

@lru_cache(maxsize=None)
def is_valid_for_interval(number, interval):
    i_min, i_max = interval
    return number >= i_min and number <= i_max

def is_valid_ticket(ticket, intervals):
    return all((is_valid(number, intervals) for number in ticket))

def simplify_names(possible_names_sets):
    # this algorithm will not work unless some columns have only one candidate
    min_length = min((len(candidates) for candidates in possible_names_sets))
    assert(min_length == 1)

    assigned_field_names = {}
    max_length = max((len(candidates) for candidates in possible_names_sets))
    while max_length > 0:
        # find columns with just one possible field
        assigned_field_names.update({candidates.pop(): index for index, candidates in enumerate(possible_names_sets) if len(candidates) == 1})
        # remove it from other columns
        for candidates in possible_names_sets:
            candidates -= set(assigned_field_names.keys())
        max_length = max((len(candidates) for candidates in possible_names_sets))
    return [name for name, order in sorted(assigned_field_names.items(), key=lambda item: item[1])]

# change the input here
file = './day16/input'
fields, my_ticket, other_tickets = parse_file(file)
intervals = get_all_intervals_from_fields(fields)

# Part 1
invalid_numbers = [number for number in numbers_from_tickets(other_tickets) if not is_valid(number, intervals)]
print(sum(invalid_numbers))

# Part 2
valid_tickets = [ticket for ticket in parse_tickets(other_tickets) if is_valid_ticket(ticket, intervals)]
nb_of_columns = len(valid_tickets[0])

# transpose valid tickets
columns = [[ticket[i] for ticket in valid_tickets] for i in range(nb_of_columns)]

field_names_for_number = get_valid_fields_for_number_checker(fields, intervals)

candidate_names_for_columns = [reduce(lambda a, b : a & b, [field_names_for_number(number) for number in column]) for column in columns]

field_names = simplify_names(candidate_names_for_columns)
my_ticket_values = parse_tickets(my_ticket)[0]

departure_fields_values = [value for value, field in zip(my_ticket_values, field_names) if field.find('departure') == 0]
print(reduce(lambda a, b: a * b, departure_fields_values, 1))