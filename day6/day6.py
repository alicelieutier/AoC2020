import sys
# import re
from functools import reduce

def parse_file(filename):
    f = open(filename)
    return f.read().split('\n\n')

def number_anyone_yes_questions(group):
    return len(set(group) - {'\n'})

def number_everyone_yes_questions(group):
    people_yes_questions = (set(yes_questions) for yes_questions in group.split('\n'))
    intersection = reduce(lambda a, b : a & b, people_yes_questions)
    return len(intersection)

# change the input here
file = './day6/input'
groups = parse_file(file)

#part 1
numbers = [number_anyone_yes_questions(group) for group in groups]
print(sum(numbers))

#part 2
numbers = [number_everyone_yes_questions(group) for group in groups]
print(sum(numbers))