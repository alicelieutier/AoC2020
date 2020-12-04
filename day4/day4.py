import sys
import re
from functools import reduce

def parse_lines(filename):
    f = open(filename)
    return f.read().split('\n\n')

FIELD_PATTERN = re.compile(r'([a-z]{3}):')
SEVEN_FIELDS = frozenset({'pid', 'iyr', 'eyr', 'hcl', 'byr', 'ecl', 'hgt'})
def has_seven_fields_present(document):
    keys = FIELD_PATTERN.findall(document)
    return set(keys) >= SEVEN_FIELDS

def valid_year(pattern, document, min_year, max_year):
    match = pattern.search(document)
    if match is None:
        return False
    year = int(match.group(1))
    return year >= min_year and year <= max_year

# byr (Birth Year) - four digits; at least 1920 and at most 2002.
BYR_PATTERN = re.compile(r'byr:(\d{4})(\s|$)')
def valid_birthyear(document):
    return valid_year(BYR_PATTERN, document, 1920, 2002)

# iyr (Issue Year) - four digits; at least 2010 and at most 2020.
IYR_PATTERN = re.compile(r'iyr:(\d{4})(\s|$)')
def valid_issue_year(document):
    return valid_year(IYR_PATTERN, document, 2010, 2020)

# eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
EYR_PATTERN = re.compile(r'eyr:(\d{4})(\s|$)')
def valid_expiration_year(document):
    return valid_year(EYR_PATTERN, document, 2020, 2030)

# hgt (Height) - a number followed by either cm or in:
# If cm, the number must be at least 150 and at most 193.
# If in, the number must be at least 59 and at most 76.
HGT_PATTERN = re.compile(r'hgt:(?P<height>\d+)(?P<unit>cm|in)(\s|$)')
def valid_height(document):
    match = HGT_PATTERN.search(document)
    if match is None:
        return False
    height = int(match.group('height'))
    unit = match.group('unit')
    return ((unit == 'cm' and height >= 150 and height <= 193)
            or (unit == 'in' and height >= 59 and height <= 76))

def valid_field_match(pattern, document):
    return pattern.search(document) is not None

# hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
HCL_PATTERN = re.compile(r'hcl:#[a-f0-9]{6}(\s|$)')
def valid_hair_color(document):
    return valid_field_match(HCL_PATTERN, document)

# ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
ECL_PATTERN = re.compile(r'ecl:(amb|blu|brn|gry|grn|hzl|oth)(\s|$)')
def valid_eye_color(document):
    return valid_field_match(ECL_PATTERN, document)

# pid (Passport ID) - a nine-digit number, including leading zeroes.
PID_PATTERN = re.compile(r'pid:\d{9}(\s|$)')
def valid_passport_ID(document):
    return valid_field_match(PID_PATTERN, document)

VALID_FIELD_CHECKERS = [
    valid_birthyear,
    valid_issue_year,
    valid_expiration_year,
    valid_height,
    valid_hair_color,
    valid_eye_color,
    valid_passport_ID,
]
def has_seven_valid_fields(document):
    return all([checker(document) for checker in VALID_FIELD_CHECKERS])

def count_valid(elements, checker):
    def aux(acc, element):
        return acc + 1 if checker(element) else acc
    return reduce(aux, elements, 0)

# change the input here
file = './day4/input'
documents = parse_lines(file)

# part 1
valid = count_valid(documents, has_seven_fields_present)
print(valid)

# part 2
valid = count_valid(documents, has_seven_valid_fields)
print(valid)