import sys
import re

def split_lines(lines):
    return [line.strip() for line in lines.split('\n')]

def parse_file(filename):
    f = open(filename)
    rules, words = f.read().split('\n\n')
    return split_lines(rules), split_lines(words)

LETTER_PATTERN = re.compile(r' "([ab])"')
NUMBER_PATTERN = re.compile(r'\d+')
def parse_rule(line):
    rule_id, rule = line.split(':')
    match = LETTER_PATTERN.search(rule)
    if match is not None:
        letter = match.group(1)
        return (rule_id, {'type': 'letter', 'letter': letter})
    possible_rules = [NUMBER_PATTERN.findall(branch) for branch in rule.split('|')]
    return (rule_id, {'type': 'numbers', 'rules': possible_rules})

def memoized_skip_first(f):
    memo = {}
    # magic number based on trial error
    # lower means faster
    # fastest that was still accurate was 8 for my input.
    NB_OF_CALLS = 8
    def helper(skip, x):
        if x not in memo:
            # Storing the result from first call
            # which means part 2 rules will default to part 1
            # rules after NB_OF_CALLS calls.
            memo[x] = [f(skip, x), 1]
        memo[x][1] += 1
        if memo[x][1] > NB_OF_CALLS:
            # returning cached part 1 result
            return memo[x][0]
        return f(skip, x)
    return helper

@memoized_skip_first
def build_pattern(rules, id):
    rule = rules[id]
    if rule['type'] == 'letter':
        return rule['letter']
    else:
        possibles = []
        for branch in rule['rules']:
            branch_letters = []
            for rule_id in branch:
                branch_letters.append(build_pattern(rules, rule_id))
            possibles.append(''.join(branch_letters))
        return '(' +'|'.join(possibles) + ')'

def check_word(pattern, word):
    match = pattern.match(word)
    return match is not None and match.end() == len(word)

# change the input here
file = './day19/input'

# Part 1
rules, words = parse_file(file)
rules_dict = {k: v for k, v in map(parse_rule, rules)}
pattern = re.compile(build_pattern(rules_dict, '0'))
print(len([word for word in words if check_word(pattern, word)]))

# Part 2
# add this to rules - now with loops!
extra_rules = ['8: 42 | 42 8', '11: 42 31 | 42 11 31']
p2_rules_dict = {k: v for k, v in map(parse_rule, rules + extra_rules)}
p2_pattern = re.compile(build_pattern(p2_rules_dict, '0'))
print(len([word for word in words if check_word(p2_pattern, word)]))
