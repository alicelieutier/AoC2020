import sys
from collections import deque

def parse_file(filename):
    f = open(filename)
    player1, player2 = f.read().split('\n\n')
    return parse_hand(player1), parse_hand(player2)

def parse_hand(hand):
    return deque([int(line) for line in hand.split('\n')[1:]])

def draw_card(hand):
    return hand.popleft()

def add_to_bottom(hand, top_card, bottom_card):
    hand.extend([top_card, bottom_card])

def copy_n(hand, n):
    return deque(list(hand)[:n])

def calculate_score(hand):
    return sum([(value * card) for value, card in zip(hand, range(len(hand), 0, -1))])

def play_standard_game(p1_hand, p2_hand):
    while (len(p1_hand) > 0 and len(p2_hand) > 0):
        p1_card = draw_card(p1_hand)
        p2_card = draw_card(p2_hand)
        if p1_card > p2_card:
            add_to_bottom(p1_hand, p1_card, p2_card)
        else:
            add_to_bottom(p2_hand, p2_card, p1_card)
    game_winner = 'p1' if len(p1_hand) > 0 else 'p2'
    return game_winner

def play_recursive_game(p1_hand, p2_hand):
    game_rounds = set()
    while (len(p1_hand) > 0 and len(p2_hand) > 0):
        # hands are the same as a previous round in game
        if (tuple(p1_hand), tuple(p2_hand)) in game_rounds:
            return 'p1'
        game_rounds |= {(tuple(p1_hand), tuple(p2_hand))}

        p1_card = draw_card(p1_hand)
        p2_card = draw_card(p2_hand)

        if len(p1_hand) >= p1_card and len(p2_hand) >= p2_card:
            round_winner = play_recursive_game(copy_n(p1_hand, p1_card), copy_n(p2_hand, p2_card))
        else:
            round_winner = 'p1' if p1_card > p2_card else 'p2'

        if round_winner == 'p1':
            add_to_bottom(p1_hand, p1_card, p2_card)
        else:
            add_to_bottom(p2_hand, p2_card, p1_card)

    game_winner = 'p1' if len(p1_hand) > 0 else 'p2'
    return game_winner

# change the input here
file = './day22/input'

# Part 1
p1_hand, p2_hand = parse_file(file)
winner = play_standard_game(p1_hand, p2_hand)
winner_hand = p1_hand if winner == 'p1' else p2_hand
print(winner, calculate_score(winner_hand))

# Part 2
p1_hand, p2_hand = parse_file(file)
winner = play_recursive_game(p1_hand, p2_hand)
winner_hand = p1_hand if winner == 'p1' else p2_hand
print(winner, calculate_score(winner_hand))

# Tests
assert(calculate_score([1,1]) == 3)
assert(calculate_score([4,3]) == 8 + 3)