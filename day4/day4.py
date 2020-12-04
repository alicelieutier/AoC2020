import sys
import re
from functools import reduce

def parse_file(filename):
    f = open(filename)
    return f.read().split('\n\n')

FIELD_PATTERN = re.compile(r'([a-z]{3}):')
SEVEN_FIELDS = frozenset({'pid', 'iyr', 'eyr', 'hcl', 'byr', 'ecl', 'hgt'})
def has_seven_fields_present(document):
    keys = FIELD_PATTERN.findall(document)
    return set(keys) >= SEVEN_FIELDS

# byr (Birth Year) - four digits; at least 1920 and at most 2002.
BYR_PATTERN = re.compile(r'byr:(\d{4})(\s|$)')
# iyr (Issue Year) - four digits; at least 2010 and at most 2020.
IYR_PATTERN = re.compile(r'iyr:(\d{4})(\s|$)')
# eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
EYR_PATTERN = re.compile(r'eyr:(\d{4})(\s|$)')

def valid_year_checker(pattern, min_year, max_year):
    def checker(document):
        match = pattern.search(document)
        if match is None:
            return False
        year = int(match.group(1))
        return year >= min_year and year <= max_year
    return checker

# hgt (Height) - a number followed by either cm or in:
# If cm, the number must be at least 150 and at most 193.
# If in, the number must be at least 59 and at most 76.
HGT_PATTERN = re.compile(r'hgt:(?P<height>\d+)(?P<unit>cm|in)(\s|$)')
def valid_height(document):
    match = HGT_PATTERN.search(document)
    if match is None:
        return False
    height, unit = int(match.group('height')), match.group('unit')
    return ((unit == 'cm' and height >= 150 and height <= 193)
            or (unit == 'in' and height >= 59 and height <= 76))

# hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
HCL_PATTERN = re.compile(r'hcl:#[a-f0-9]{6}(\s|$)')
# ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
ECL_PATTERN = re.compile(r'ecl:(amb|blu|brn|gry|grn|hzl|oth)(\s|$)')
# pid (Passport ID) - a nine-digit number, including leading zeroes.
PID_PATTERN = re.compile(r'pid:\d{9}(\s|$)')

def valid_field_checker(pattern):
    return lambda document : pattern.search(document) is not None

VALIDITY_CHECKERS = [
    valid_year_checker(BYR_PATTERN, 1920, 2002),
    valid_year_checker(IYR_PATTERN, 2010, 2020),
    valid_year_checker(EYR_PATTERN, 2020, 2030),
    valid_height,
    valid_field_checker(HCL_PATTERN),
    valid_field_checker(ECL_PATTERN),
    valid_field_checker(PID_PATTERN),
]

def has_seven_valid_fields(document):
    return all([checker(document) for checker in VALIDITY_CHECKERS])

def count_valid(elements, checker):
    def aux(acc, element):
        return acc + 1 if checker(element) else acc
    return reduce(aux, elements, 0)

# change the input here
file = './day4/input'
documents = parse_file(file)

# part 1
valid = count_valid(documents, has_seven_fields_present)
print(valid)

# part 2
valid = count_valid(documents, has_seven_valid_fields)
print(valid)