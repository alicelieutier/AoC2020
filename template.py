import sys
# import re
# from functools import reduce, lru_cache
# from collections import deque
# from itertools import count, islice

def parse_things(filename):
    f = open(filename)
    return [parse_thing(line.strip()) for line in f.readlines()]

LINE_PATTERN = re.compile(r'hgt:(?P<height>\d+)(?P<unit>cm|in)(\s|$)')
def parse_thing(line):
    match = LINE_PATTERN.search(line)
    height, unit = int(match.group('height')), match.group('unit')
    return (height, unit)

# change the input here
file = './dayX/input'
things = parse_things(file)
