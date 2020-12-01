import sys

def get_lines_as_number(filename):
    f = open(filename)
    return [int(line.strip()) for line in f.readlines()]

def find_pair(numbers, target):
    seen = set()
    for number in numbers:
        missing_pair = target - number
        if missing_pair in seen:
            return(number, missing_pair)
        seen.add(number)

def find_triplet(numbers, target):
    seen = set()
    for a in numbers:
        for b in numbers:
            missing_c = target - (a + b)
            if missing_c in seen:
                return a, b, missing_c
            seen.add(a)

file = './day1/input'
numbers = get_lines_as_number(file)

# part 1
a, b = find_pair(numbers, 2020)
print(a * b)

# part 2
a, b, c = find_triplet(numbers, 2020)
print(a * b * c)