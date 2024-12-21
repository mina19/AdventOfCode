## Pull Data
from pathlib import Path
from collections import defaultdict, deque
from get_data import save_data, timeit
from itertools import product

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


def find_all_shortest_paths(grid, start_pos, end_char):
    queue = deque([(start_pos, "")])
    level = 0
    paths_at_level = defaultdict(list)  # Track paths by level
    visited = {start_pos: level}  # Track level at which position was first visited
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    found_target = False
    target_level = float("inf")

    while queue:
        current_pos, instructions = queue.popleft()
        level = len(instructions) // 2  # Each move is two chars (direction + 'A')

        # If this path is longer than a path we already found, stop
        if level > target_level:
            break

        current_row, current_col = current_pos

        # If we found the target
        if grid[current_row][current_col] == end_char:
            found_target = True
            target_level = level
            paths_at_level[level].append((instructions, current_pos))
            continue

        # Try all directions
        for drow, dcol in directions:
            new_row, new_col = current_row + drow, current_col + dcol
            new_pos = (new_row, new_col)

            # If valid position
            if grid[new_row][new_col] != "!":
                # Can visit if never visited or visited at same level
                if new_pos not in visited or visited[new_pos] == level + 1:
                    visited[new_pos] = level + 1
                    direction_symbol = movement_reverse_dict[(drow, dcol)]
                    new_instructions = instructions + direction_symbol
                    queue.append((new_pos, new_instructions))

    return paths_at_level[target_level] if found_target else [("", start_pos)]


def find_numerical_robot_instructions(code):
    start_pos = (3, 2)
    paths_by_step = []
    for _, char in enumerate(code):
        all_results = find_all_shortest_paths(numeric_keypad, start_pos, char)
        start_pos = all_results[0][1]
        min_length = min(len(x[0]) for x in all_results)
        shortest_tuples = [t for t in all_results if len(t[0]) == min_length]
        paths_by_step.append(shortest_tuples)
        print(shortest_tuples)
        # instructions, start_pos = find_all_shortest_paths(numeric_keypad, start_pos, char)
        # full_instructions += instructions
    return full_instructions


def find_directional_robot_instructions(code):
    start_pos = (0, 2)
    full_instructions = ""
    for _, char in enumerate(code):
        instructions, start_pos = find_shortest_path(
            directional_keypad, start_pos, char
        )
        full_instructions += instructions
    return full_instructions


## Part 1
@timeit
def part1():
    result = 0

    for code in data:
        # Find what needs to be pressed for robot1
        robot1_instructions = find_numerical_robot_instructions(code)
        robot2_instructions = find_directional_robot_instructions(robot1_instructions)
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
