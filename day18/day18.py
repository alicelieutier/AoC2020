import sys
from operator import add, mul
from functools import reduce

def parse_lines(filename):
    f = open(filename)
    return [line.strip() for line in f.readlines()]

def evaluate_line_part1(line):
    total, _ = evaluate_expr_part1(line)
    return total

def evaluate_expr_part1(expr, current_index = 0, total = 0, operator = add):
    # base case
    if current_index >= len(expr) or expr[current_index] == ')':
        return total, current_index
    # recursion
    character = expr[current_index]
    if character in '+*':
        operator = add if character == '+' else mul
    elif character in '1234567890':
        total = operator(total, int(character))
    elif character == '(':
        token, current_index = evaluate_expr_part1(expr, current_index + 1)
        total = operator(total, token)
    return evaluate_expr_part1(expr, current_index + 1, total, operator)

def evaluate_line_part2(line):
    total, _ = evaluate_expr_part2(line)
    return total

def update_counters_add(total, to_multiply, token):
    return total + token, to_multiply

def update_counters_mul(total, to_multiply, token):
    return token, total * to_multiply

def evaluate_expr_part2(
    expr,
    current_index = 0,
    total = 0,
    to_multiply = 1,
    operator = update_counters_add
):
     # base case
    if current_index >= len(expr) or expr[current_index] == ')':
        return total * to_multiply, current_index
    # recursion
    character = expr[current_index]
    if character in '+*':
        operator = update_counters_add if character == '+' else update_counters_mul
    elif character in '1234567890':
        total, to_multiply = operator(total, to_multiply, int(character))
    elif character == '(':
        token, current_index = evaluate_expr_part2(expr, current_index + 1)
        total, to_multiply = operator(total, to_multiply, token)
    return evaluate_expr_part2(expr, current_index + 1, total, to_multiply, operator)

# change the input here
file = './day18/input'
lines = parse_lines(file)

# We observe that all numbers in the input only have one digit
# Part 1
print(reduce(lambda acc, line: acc + evaluate_line_part1(line), lines, 0))

# Part 2
print(reduce(lambda acc, line: acc + evaluate_line_part2(line), lines, 0))

# Tests
assert(evaluate_line_part1('1 + 2 * 3 + 4 * 5 + 6') == 71)
assert(evaluate_line_part1('2 * 3 + (4 * 5)') == 26)
assert(evaluate_line_part1('5 + (8 * 3 + 9 + 3 * 4 * 3)') == 437)
assert(evaluate_line_part1('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))') == 12240)
assert(evaluate_line_part1('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2') == 13632)
assert(evaluate_line_part1('(3 * 4) + (4 * 5)') == 12 + 20)
assert(evaluate_line_part1('3 * (4 + 4) * 5') == 3 * 8 * 5)
assert(evaluate_line_part1('3 * (((4 + 4)) + 5)') == 3 * (8 + 5))

assert(evaluate_line_part2('1 + 2 * 3 + 4 * 5 + 6') == 3*7*11)
assert(evaluate_line_part2('1 + (2 * 3) + (4 * (5 + 6))') == 51)
assert(evaluate_line_part2('2 * 3 + (4 * 5)') == 46)
assert(evaluate_line_part2('5 + (8 * 3 + 9 + 3 * 4 * 3)') == 1445)
assert(evaluate_line_part2('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))') == 669060)
assert(evaluate_line_part2('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2') == 23340)