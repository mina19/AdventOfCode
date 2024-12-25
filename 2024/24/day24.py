## Pull Data
from pathlib import Path

from get_data import save_data, timeit

save_data(2024, day := 24)
data = Path(f"2024/{day}/day{day:02d}.txt").read_text()
# data = Path(f"2024/{day}/day{day:02d}_sample.txt").read_text()

data_parts = data.split("\n\n")

wires = {}
for line in data_parts[0].splitlines():
    wire, value = line.split(": ")
    wires[wire] = value == "1"

## Part 1
@timeit
def part1():
    unprocessed_wires = data_parts[1].splitlines()
    new_unprocessed_wires = []

    while unprocessed_wires:
        for line in unprocessed_wires:
            # Example: x00 AND y00 -> z00 becomes ['x00', 'AND', 'y00', '->', 'z00']
            wire1, operation, wire2, _, wire3 = line.split(" ")
            if wire1 not in wires or wire2 not in wires:
                new_unprocessed_wires.append(line)
                continue

            # AND gates output 1 if both inputs are 1; if either input is 0, these gates output 0.
            # OR gates output 1 if one or both inputs is 1; if both inputs are 0, these gates output 0.
            # XOR gates output 1 if the inputs are different; if the inputs are the same, these gates output 0.
            if operation == "AND":
                wires[wire3] = wires[wire1] and wires[wire2]
            elif operation == "OR":
                wires[wire3] = wires[wire1] or wires[wire2]
            elif operation == "XOR":
                wires[wire3] = wires[wire1] != wires[wire2]

        unprocessed_wires = new_unprocessed_wires
        new_unprocessed_wires = []

    # Gets all wires starting with "z", sort them alphabetically in reverse order
    result = ''.join('1' if wires[k] else '0' for k in sorted([k for k in wires if k.startswith('z')], reverse=True))

    return int(result, 2)


print(part1())


## Part 2
@timeit
def part2():
    pass


part2()
