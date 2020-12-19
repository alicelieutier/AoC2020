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
    def helper(skip, x):
        if x not in memo:
            memo[x] = f(skip, x)
        return memo[x]
    return helper 

@memoized_skip_first
def expand_rules(rules, id):
    rule = rules[id]
    if rule['type'] == 'letter':
        return rule['letter']
    else:
        possibles = []
        for branch in rule['rules']:
            branch_letters = []
            for rule_id in branch:
                branch_letters.append(expand_rules(rules, rule_id))
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
pattern = re.compile(expand_rules(rules_dict, '0'))
print(len([word for word in words if check_word(pattern, word)]))