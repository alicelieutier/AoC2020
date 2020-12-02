import sys
import re
from functools import reduce

def parse_lines(filename):
    f = open(filename)
    return [tuple(line.strip().split(': ')) for line in f.readlines()]

def parse_policy(policy):
    pattern = re.compile("[- ]")
    min_nb, max_nb, letter = tuple(pattern.split(policy))
    return int(min_nb), int(max_nb), letter

def is_valid_password(line):
    policy, password = line
    min_nb, max_nb, letter = parse_policy(policy)
    occurrences = password.count(letter)
    return occurrences >= min_nb and occurrences <= max_nb

def is_valid_password_part2(line):
    policy, password = line
    i1, i2, letter = parse_policy(policy)
    # the index in the policy are 1-indexed
    return (password[i1-1] == letter) ^  (password[i2-1] == letter)

def count_valid(lines, checker):
    def aux(acc, line):
        return acc + 1 if checker(line) else acc
    return reduce(aux, lines, 0)


# change the input here
file = './day2/input'
lines = parse_lines(file)

# part 1
print(count_valid(lines, is_valid_password))

# part 2
print(count_valid(lines, is_valid_password_part2))