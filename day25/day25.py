from functools import lru_cache

TEST_INPUT = (5764801, 17807724)
INPUT = (9093927, 11001876)

@lru_cache(maxsize=None)
def transform_number_rec(number, loop_size):
    if loop_size == 0:
        return 1
    return (transform_number(number, loop_size - 1) * number) % 20201227

def transform_number(number, loop_size):
    n = 1
    for _ in range(loop_size):
        n *= number
        n = n % 20201227
    return n

card, door = INPUT
i = 1
transformed = transform_number_rec(7, i)
while transformed not in (card, door):
    i += 1
    transformed = transform_number_rec(7, i)

if transformed == card:
    print(transform_number(door, i))
else:
    print(transform_number(card, i))

# Tests
assert(transform_number(7, 8) == 5764801)