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
    final_pos = (0, 0)
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
            final_pos = current_pos
            paths_at_level[level].append(instructions)
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

    return (paths_at_level[target_level], final_pos) if found_target else None


def find_numeric_robot_instructions(code):
    start_pos = (3, 2)
    paths_by_step = []
    for _, char in enumerate(code):
        all_results = find_all_shortest_paths(numeric_keypad, start_pos, char)
        if all_results:
            start_pos = all_results[1]
            min_length = min(len(x) for x in all_results[0])
            shortest_tuples = [t + "A" for t in all_results[0] if len(t) == min_length]
            paths_by_step.append(shortest_tuples)
    instruction_candidates = ["".join(combo) for combo in product(*paths_by_step)]
    return instruction_candidates


def find_directional_robot_instructions(code):
    start_pos = (0, 2)
    paths_by_step = []
    for _, char in enumerate(code):
        all_results = find_all_shortest_paths(directional_keypad, start_pos, char)
        if all_results:
            start_pos = all_results[1]
            min_length = min(len(x) for x in all_results[0])
            shortest_tuples = [t + "A" for t in all_results[0] if len(t) == min_length]
            paths_by_step.append(shortest_tuples)
        instruction_candidates = ["".join(combo) for combo in product(*paths_by_step)]
    return instruction_candidates


## Part 1
@timeit
def part1():
    result = 0

    for code in data:
        # Find what needs to be pressed for robot1
        robot1_instructions = find_numeric_robot_instructions(code)

        robot2_instructions = []
        robot3_instructions = []
        for robot1_instruction in robot1_instructions:
            robot2_instruction = find_directional_robot_instructions(robot1_instruction)
            robot2_instructions.append(robot2_instruction)
            robot3_instruction = find_directional_robot_instructions(robot2_instruction)
            robot3_instructions.append(robot3_instruction)
            print(robot2_instruction, robot3_instruction)
            print("done")

        # min_length = min(len(x) for x in robot2_instructions)
        # shortest_robot2_instructions = [
        #     t for t in robot2_instructions if len(t) == min_length
        # ]

        robot3_instructions = []
        for robot2_instruction in robot2_instructions:
            robot3_instruction = find_directional_robot_instructions(robot2_instruction)
            robot3_instructions.append(robot3_instruction)
            print(robot3_instruction)

        min_length = min(len(x) for x in robot3_instructions)
        shortest_robot3_instructions = [
            t for t in robot3_instructions if len(t) == min_length
        ]

        print(shortest_robot3_instructions)
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
