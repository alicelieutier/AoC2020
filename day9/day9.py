import sys
from collections import deque

def parse_numbers(filename):
    f = open(filename)
    return [int(line.strip()) for line in f.readlines()]

def sum_in_window(window, target):
    seen = set()
    for number in window:
        missing_pair = target - number
        if missing_pair in seen:
            return True
        seen.add(number)
    return False

def find_first_attack(numbers, preamble_length):
    window = deque(numbers[:preamble_length])
    for number in numbers[preamble_length:]:
        if not sum_in_window(window, number):
            return number
        window.popleft()
        window.append(number)

# using two pointers method to keep track
# of window
def subsequence_sum(numbers, target):
    left, right = 0, 1 # including window
    current_sum = numbers[left] + numbers[right]
    while left <= right:
        if current_sum == target:
            return numbers[left:right+1]
        elif current_sum < target:
            right += 1
            current_sum += numbers[right]
        else: # current_sum > target:
            current_sum -= numbers[left]
            left += 1

# change the input here
file = './day9/input'
numbers = parse_numbers(file)

# part 1
target = find_first_attack(numbers, 25)
print(target)

# part 2
subsequence = subsequence_sum(numbers, target)
print(min(subsequence) + max(subsequence))
