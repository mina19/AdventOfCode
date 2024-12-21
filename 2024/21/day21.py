## Pull Data
from pathlib import Path
from collections import defaultdict
from get_data import save_data, timeit

save_data(2024, day := 21)
data = Path(f"2024/{day}/day{day:02d}.txt").read_text()
data = Path(f"2024/{day}/day{day:02d}_sample.txt").read_text()

# Information:

# Numeric keypad
# +---+---+---+
# | 7 | 8 | 9 |
# +---+---+---+
# | 4 | 5 | 6 |
# +---+---+---+
# | 1 | 2 | 3 |
# +---+---+---+
#     | 0 | A |
#     +---+---+
#           ^ Starting position for robot 1

# Directional keypad
#     +---+---+
#     | ^ | A | < Starting position for robot 2
# +---+---+---+
# | < | v | > |
# +---+---+---+

# Directional keypad
#     +---+---+
#     | ^ | A | < Starting position for robot 3
# +---+---+---+
# | < | v | > |
# +---+---+---+

# Directional keypad
#     +---+---+
#     | ^ | A |
# +---+---+---+
# | < | v | > |
# +---+---+---+

numeric_keypad_values = [
    [7, 8, 9],
    [4, 5, 6],
    [1, 2, 3],
    ["", 0, "A"],
]

directional_keypad_values = [["", "^", "A"], ["<", "v", ">"]]

numeric_keypad = defaultdict(lambda: defaultdict(lambda: "!"))
for row in range(len(numeric_keypad_values)):
    for col in range(len(numeric_keypad_values[row])):
        numeric_keypad[row][col] = numeric_keypad_values[row][col]

directional_keypad = defaultdict(lambda: defaultdict(lambda: "!"))
for row in range(len(directional_keypad_values)):
    for col in range(len(directional_keypad_values[row])):
        directional_keypad[row][col] = directional_keypad_values[row][col]


## Part 1
@timeit
def part1():
    pass


part1()


## Part 2
@timeit
def part2():
    pass


part2()
