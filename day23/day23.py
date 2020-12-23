from collections import deque
from itertools import zip_longest, tee

def parse_input_part_1(iterable):
    circle = make_circle([int(digit) for digit in iterable])
    return int(iterable[0]), circle

def parse_input_part_2(iterable, max_nb):
    digits = [int(digit) for digit in iterable]
    numbers = (n if d is None else d for (d, n) in zip_longest(digits, range(1, max_nb + 1)))
    circle = make_circle(numbers)
    return digits[0], circle

def make_circle(iterable):
    cups, next_cups = tee(iterable)
    first = next(next_cups)
    circle = {cup: next_cup for cup, next_cup in zip_longest(cups, next_cups, fillvalue=first)}
    return circle

def pretty_format(current, circle):
    formatted = ['({})'.format(str(current))]
    next_cup = circle[current]
    while next_cup != current:
        formatted.append(str(next_cup))
        next_cup = circle[next_cup]
    return ', '.join(formatted)

def part1_answer_format(circle):
    formatted = []
    next_cup = circle[1]
    while next_cup != 1:
        formatted.append(str(next_cup))
        next_cup = circle[next_cup]
    return ''.join(formatted)

def pick_three_after(current, circle):
    one = circle[current]
    two = circle[one]
    three = circle[two]
    circle[current] = circle[three]
    return (one, two, three), circle

def insert_three_after(destination, picked, circle):
    (one, _, three) = picked
    circle[destination], circle[three] = one, circle[destination]
    return circle

def find_destination(current, picked, max_number):
    destination = current - 1 if current > 1 else max_number
    while destination in picked:
        destination = destination - 1 if destination > 1 else max_number
    return destination

def play_turn(current, circle, max_number):
    picked, circle = pick_three_after(current, circle)
    destination = find_destination(current, picked, max_number)
    circle = insert_three_after(destination, picked, circle)
    current = circle[current]
    return current, circle

def play_n_turns(current, circle, n):
    max_number = len(circle)
    for _ in range(1, n + 1):
        current, circle = play_turn(current, circle, max_number)
    return circle

TEST_INPUT = '389125467'
INPUT = '327465189'

# Part 1
current, circle = parse_input_part_1(INPUT)
circle = play_n_turns(current, circle, 100)   
print(part1_answer_format(circle))

# Part 2
current, circle = parse_input_part_2(INPUT, 1000000)
circle = play_n_turns(current, circle, 10000000) 
star_1 = circle[1]
star_2 = circle[star_1]
print(star_1 * star_2)