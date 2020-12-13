import sys
from functools import reduce

def parse_file(filename):
    f = open(filename)
    timestamp_str, buses_str = f.readlines()
    timestamp = int(timestamp_str.strip())
    buses = [(int(bus_id), index) for index, bus_id in enumerate(buses_str.strip().split(',')) if bus_id != 'x']
    return timestamp, buses

def wait_time_till_bus(timestamp, bus_id):
    return (bus_id - timestamp) % bus_id

def is_valid_timestamp_for_bus(bus, timestamp):
    bus_id, wait = bus
    return (timestamp + wait) % bus_id == 0

# Observation - all bus ids are prime
def find_timestamp_for_buses(buses):
    def aux(acc, bus):
        timestamp, factors_until_now = acc
        bus_id, _ = bus
        while not is_valid_timestamp_for_bus(bus, timestamp):
            # Trying to get to this new modulo by only adding multiples
            # of the previous factors to not disturb the previous modulo.
            timestamp += factors_until_now
        return timestamp, factors_until_now * bus_id
    return reduce(aux, buses, (0, 1))

# change the input here
file = './day13/input'
closest_timestamp, buses = parse_file(file)

# Part 1
wait_time, bus_id = min([(wait_time_till_bus(closest_timestamp, bus_id), bus_id) for bus_id, _ in buses])
print(bus_id * wait_time)

# Part 2
timestamp, _ = find_timestamp_for_buses(buses)
print(timestamp)

# Tests
assert(wait_time_till_bus(49, 7) == 0)
assert(wait_time_till_bus(50, 7) == 6)
assert(wait_time_till_bus(48, 7) == 1)
assert(wait_time_till_bus(52, 7) == 4)
assert(wait_time_till_bus(939, 59) == 5)
assert(wait_time_till_bus(939, 13) == 10)