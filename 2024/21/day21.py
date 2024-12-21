## Pull Data
from pathlib import Path
from collections import defaultdict, deque
from get_data import save_data, timeit

save_data(2024, day := 21)
data = Path(f"2024/{day}/day{day:02d}.txt").read_text().splitlines()
data = Path(f"2024/{day}/day{day:02d}_sample.txt").read_text().splitlines()

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
    ["!", "0", "A"],
]

directional_keypad_values = [["!", "^", "A"], ["<", "v", ">"]]

numeric_keypad = defaultdict(lambda: defaultdict(lambda: "!"))
for row in range(len(numeric_keypad_values)):
    for col in range(len(numeric_keypad_values[row])):
        numeric_keypad[row][col] = numeric_keypad_values[row][col]

directional_keypad = defaultdict(lambda: defaultdict(lambda: "!"))
for row in range(len(directional_keypad_values)):
    for col in range(len(directional_keypad_values[row])):
        directional_keypad[row][col] = directional_keypad_values[row][col]

movement_dict = {
    "<": (0, -1),
    "^": (-1, 0),
    ">": (0, 1),
    "v": (1, 0),
    "A": (0, 0),
}

movement_reverse_dict = {val: key for key, val in movement_dict.items()}


# Check robot 1 movements
def numeric_robot(movements):
    robot_movements = [char for char in movements]

    robot_row, robot_col = (3, 2)
    robot_output = ""
    for movement in robot_movements:
        drow, dcol = movement_dict[movement]
        robot_row += drow
        robot_col += dcol
        if movement == "A":  # Pushing a button
            robot_output += numeric_keypad[robot_row][robot_col]
    return robot_output


# Check robot 2, 3 movements
def directional_robot(movements):
    robot_movements = [char for char in movements]

    robot_row, robot_col = (0, 2)
    robot_output = ""
    for movement in robot_movements:
        drow, dcol = movement_dict[movement]
        robot_row += drow
        robot_col += dcol
        if movement == "A":  # Pushing a button
            robot_output += directional_keypad[robot_row][robot_col]
    return robot_output


def check_instructions(instructions, code):
    robot2_instructions = directional_robot(instructions)
    robot1_instructions = directional_robot(robot2_instructions)
    return_code = numeric_robot(robot1_instructions)
    return return_code == code


sample_code_solutions = {
    "029A": "<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A",
    "980A": "<v<A>>^AAAvA^A<vA<AA>>^AvAA<^A>A<v<A>A>^AAAvA<^A>A<vA>^A<A>A",
    "179A": "<v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A",
    "456A": "<v<A>>^AA<vA<A>>^AAvAA<^A>A<vA>^A<A>A<vA>^A<A>A<v<A>A>^AAvA<^A>A",
    "379A": "<v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A",
}


def find_shortest_path(grid, start_pos, end_char):
    queue = deque([(start_pos, "")])
    visited = {start_pos}
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    while queue:
        (current_row, current_col), instructions = queue.pop()

        # If we found the target number
        if grid[current_row][current_col] == end_char:
            return instructions, (current_row, current_col)

        # Try all directions
        for drow, dcol in directions:
            new_row, new_col = current_row + drow, current_col + dcol

            # If valid position and not visited
            if grid[new_row][new_col] != "!" and (new_row, new_col) not in visited:
                visited.add((new_row, new_col))
                direction_symbol = movement_reverse_dict[(drow, dcol)]
                updated_instructions = instructions + direction_symbol + "A"
                queue.appendleft(((new_row, new_col), updated_instructions))

    return "", start_pos


def find_numerical_robot_instructions(code):
    start_pos = (3, 2)
    full_instructions = ""
    for index, char in enumerate(code):
        instructions, start_pos = find_shortest_path(numeric_keypad, start_pos, char)
        full_instructions += instructions
    return full_instructions


## Part 1
@timeit
def part1():
    result = 0

    for code in data:
        # Find what needs to be pressed for robot1
        robot1_instructions = find_numerical_robot_instructions(code)
        print(robot1_instructions)
        instructions = sample_code_solutions[code]

        if check_instructions(instructions, code):
            result += len(instructions) * int("".join(filter(str.isdigit, code)))

    return result


print(part1())


## Part 2
@timeit
def part2():
    pass


part2()
