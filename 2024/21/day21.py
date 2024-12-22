## Pull Data
from collections import defaultdict, deque
from functools import cache
from itertools import combinations, pairwise, product
from pathlib import Path

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

movement_dict = {(0, -1): '<', (-1, 0): '^', (0, 1): '>', (1, 0): 'v', (0, 0): 'A'}


@cache
def find_all_shortest_paths(start_pos, end_char, grid_type="numeric"):
   # Initialize queue and tracking variables
   queue = deque([(start_pos, "")]) # Track position and path
   paths_at_level = defaultdict(list)
   visited = {start_pos: 0}  # Position -> level mapping
   target_level = float("inf")
   final_pos = None
   found_target = False
   grid = numeric_keypad if grid_type == "numeric" else directional_keypad
   
   while queue:
       (current_row, current_col), instructions = queue.popleft()
       level = len(instructions)
       
       # Stop if path is longer than shortest found
       if level > target_level:
           break
           
       # Check if we found target
       if grid[current_row][current_col] == end_char:
           found_target = True
           target_level = level
           final_pos = (current_row, current_col)
           paths_at_level[level].append(instructions)
           continue
           
       # Try each direction
       for direction in movement_dict:
           drow, dcol = direction
           new_row, new_col = current_row + drow, current_col + dcol
           new_pos = (new_row, new_col)
           
           # Check if move is valid
           if grid[new_row][new_col] != "!":
               # Only visit if new or at same level
               if new_pos not in visited or visited[new_pos] == level + 1:
                   visited[new_pos] = level + 1
                   new_instructions = instructions + movement_dict[(drow, dcol)]
                   queue.append((new_pos, new_instructions))
   
   return (paths_at_level[target_level], final_pos) if found_target else None


def find_robot_instructions(code, instruction_type = "numeric"):
    start_pos = (3, 2) if instruction_type == "numeric" else (0,2)
    paths_by_step = []
    for _, char in enumerate(code):
        all_results = find_all_shortest_paths(start_pos, char, instruction_type)
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
        robot_instruction = find_robot_instructions(instruction, "directional")
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
        robot1_instructions = find_robot_instructions(code, "numeric")

        instructions = robot1_instructions
        for _ in range(n):
            instructions = direction_robot_instructions(instructions)

        result += len(instructions[0]) * int("".join(filter(str.isdigit, code)))

    return result


## Part 1
print(solve(2))


## Part 2
# Better solution is to hash direction instructions from every starting point
# on the directional keypad to every end point
# Need more time to do this later
def build_shortest_paths_dict():
    paths_dict = {}
    positions = []
    
    # Get all valid positions from the grid
    for row in directional_keypad:
        for col in directional_keypad[row]:
            if directional_keypad[row][col] != "!":
                positions.append((row, col))
    
    # Get all valid characters we might want to move to
    valid_chars = set(directional_keypad[row][col] 
                     for row in directional_keypad 
                     for col in directional_keypad[row] 
                     if directional_keypad[row][col] != "!")
    
    # Find all shortest paths from each position to each character
    for start_pos in positions:
        for end_char in valid_chars:
            result = find_all_shortest_paths(start_pos, end_char, "directional")
            if result:
                paths, _ = result
                # Keep only the shortest paths!
                paths = [s for s in paths if len(s) == min(len(x) for x in paths)]
                paths_dict[(directional_keypad[start_pos[0]][start_pos[1]], end_char)] = paths
    
    return paths_dict

paths_dict = build_shortest_paths_dict()


@timeit
def part2(n):
    result = 0

    for code in data:
        # Find what needs to be pressed for robot1
        robot1_instructions = find_robot_instructions(code, "numeric")

        instructions = robot1_instructions
        for _ in range(n):
            instruction_dict = {}
            # Add up path to traverse instruction
            for instruction in instructions:
                start_path = [path + 'A' for path in paths_dict['A', instruction[0]]]
                paths_by_step = [start_path]
                for char1, char2 in pairwise(instruction):
                    paths = paths_dict[(char1, char2)]
                    paths= [path + "A" for path in paths]
                    paths_by_step.append(paths)
                for path in ["".join(combo) for combo in product(*paths_by_step)]:
                    instruction_dict[path] = len(path)
        
            instructions = [k for k, v in instruction_dict.items() if v == min(instruction_dict.values())]

        result += len(instructions[0]) * int("".join(filter(str.isdigit, code)))

    return result


print(part2(2))