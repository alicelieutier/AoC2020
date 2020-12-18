import sys
# import re
# from functools import reduce, lru_cache
# from collections import deque
# from itertools import count, islice

def parse_lines(filename):
    f = open(filename)
    return [line.strip() for line in f.readlines()]

# we observe that all numbers in the input only have one digit
def evaluate_expr_part_1(expr, start = None):
    if start is None:
        start = 0
    offset = start
    total = 0
    operator = '+'
    while offset < len(expr) and expr[offset] != ')':
        if expr[offset] in ' ':
            offset += 1
        elif expr[offset] in '+*':
            operator = expr[offset]
            offset += 1
        elif expr[offset] in '1234567890':
            if operator == '+':
                total += int(expr[offset])
            else:
                total *= int(expr[offset])
            offset += 1
        elif expr[offset] == '(':
            token, offset = evaluate_expr_part_1(expr, offset + 1)
            if operator == '+':
                total += token
            else:
                total *= token
        else:
            print('ERROR: unexpected character', expr[offset])
    return total, offset + 1

def evaluate_expr_part_2(expr, start = None):
    if start is None:
        start = 0
    offset = start
    operator = '+'
    to_add = 0
    to_multiply = 1
    while offset < len(expr) and expr[offset] != ')':
        if expr[offset] in ' ':
            offset += 1
        elif expr[offset] in '+*':
            operator = expr[offset]
            offset += 1
        elif expr[offset] in '1234567890':
            if operator == '+':
                to_add += int(expr[offset])
            else:
                to_multiply *= to_add 
                to_add = int(expr[offset])
            offset += 1
        elif expr[offset] == '(':
            token, offset = evaluate_expr_part_2(expr, offset + 1)
            if operator == '+':
                to_add += token
            else:
                to_multiply *= to_add
                to_add = token
        else:
            print('ERROR: unexpected character', expr[offset])
    return to_add * to_multiply, offset + 1

# change the input here
file = './day18/input'
lines = parse_lines(file)

# Part 1
print(sum([evaluate_expr_part_1(line)[0] for line in lines]))

# Part 2
print(sum([evaluate_expr_part_2(line)[0] for line in lines]))

# Tests
assert(evaluate_expr_part_1('1 + 2 * 3 + 4 * 5 + 6')[0] == 71)
assert(evaluate_expr_part_1('2 * 3 + (4 * 5)')[0] == 26)
assert(evaluate_expr_part_1('5 + (8 * 3 + 9 + 3 * 4 * 3)')[0] == 437)
assert(evaluate_expr_part_1('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))')[0] == 12240)
assert(evaluate_expr_part_1('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2')[0] == 13632)
assert(evaluate_expr_part_1('(3 * 4) + (4 * 5)')[0] == 12 + 20)
assert(evaluate_expr_part_1('3 * (4 + 4) * 5')[0] == 3 * 8 * 5)

assert(evaluate_expr_part_2('1 + 2 * 3 + 4 * 5 + 6')[0] == 3*7*11)
assert(evaluate_expr_part_2('1 + (2 * 3) + (4 * (5 + 6))')[0] == 51)
assert(evaluate_expr_part_2('2 * 3 + (4 * 5)')[0] == 46)
assert(evaluate_expr_part_2('5 + (8 * 3 + 9 + 3 * 4 * 3)')[0] == 1445)
assert(evaluate_expr_part_2('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))')[0] == 669060)
assert(evaluate_expr_part_2('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2')[0] == 23340)