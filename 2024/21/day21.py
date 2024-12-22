## Pull Data
from pathlib import Path
from collections import defaultdict, deque
from get_data import save_data, timeit
from itertools import product
from functools import cache

save_data(2024, day := 21)
data = Path(f"2024/{day}/day{day:02d}.txt").read_text().splitlines()
# data = Path(f"2024/{day}/day{day:02d}_sample.txt").read_text().splitlines()

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


# Generalized directional robot results
def direction_robot_instructions(instructions):
    robot_instructions = []
    for instruction in instructions:
        robot_instruction = find_directional_robot_instructions(instruction)
        robot_instructions += robot_instruction

    min_length = min(len(x) for x in robot_instructions)
    shortest_robot_instructions = [
        t for t in robot_instructions if len(t) == min_length
    ]
    return shortest_robot_instructions


@timeit
def solve(n):
    result = 0

    for code in data:
        # Find what needs to be pressed for robot1
        robot1_instructions = find_numeric_robot_instructions(code)

        instructions = robot1_instructions
        for i in range(n):
            instructions = direction_robot_instructions(instructions)

        result += len(instructions[0]) * int("".join(filter(str.isdigit, code)))

    return result


## Part 1
print(solve(2))


## Part 2
print(solve(25))
