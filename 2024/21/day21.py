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
#     | ^ | A | < Starting position for me
# +---+---+---+
# | < | v | > |
# +---+---+---+

numeric_keypad_values = [
    ["7", "8", "9"],
    ["4", "5", "6"],
    ["1", "2", "3"],
    ["", "0", "A"],
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

movement_dictionary = {
    "<": (0, -1),
    "^": (-1, 0),
    ">": (0, 1),
    "v": (1, 0),
    "A": (0, 0),
}


# Check robot 1 movements
def numeric_robot(movements):
    robot1_movements = [char for char in movements]

    robot1_row, robot1_col = (3, 2)
    robot1_output = ""
    for movement in robot1_movements:
        drow, dcol = movement_dictionary[movement]
        robot1_row += drow
        robot1_col += dcol
        if movement == "A":  # Pushing a button
            robot1_output += numeric_keypad[robot1_row][robot1_col]
    return robot1_output


# Check robot 2, 3 movements
def directional_robot(movements):
    robot2_movements = [char for char in movements]

    robot2_row, robot2_col = (0, 2)
    robot2_output = ""
    for movement in robot2_movements:
        drow, dcol = movement_dictionary[movement]
        robot2_row += drow
        robot2_col += dcol
        if movement == "A":  # Pushing a button
            robot2_output += directional_keypad[robot2_row][robot2_col]
    return robot2_output


## Part 1
@timeit
def part1():
    robot2_instructions = directional_robot(
        "<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A"
    )
    robot1_instructions = directional_robot(robot2_instructions)
    return numeric_robot(robot1_instructions)


print(part1())


## Part 2
@timeit
def part2():
    pass


part2()
