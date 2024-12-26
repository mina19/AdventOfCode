## Pull Data
from collections import defaultdict
from pathlib import Path

from get_data import save_data, timeit

save_data(2024, day := 15)
data = Path(f"2024/{day}/day{day:02d}.txt").read_text()
# data = Path(f"2024/{day}/day{day:02d}_sample.txt").read_text()

# Get the robot movements
movements = data.split("\n\n")[1].replace("\n", "")

# Warehouse maps for part 1 and part 2
warehouse_map = data.split("\n\n")[0].splitlines()
warehouse_map_dict = defaultdict(
    lambda: defaultdict(lambda: "!"),
    enumerate(defaultdict((lambda: "!"), enumerate(line)) for line in warehouse_map),
)
rows = len(warehouse_map)
cols = len(warehouse_map[0])


# Expand the map
def expand_map(char):
    if char == "O":
        return "[]"
    elif char == "@":
        return "@."
    else:
        return char + char


warehouse_map_part2 = [
    "".join(expand_map(char) for char in line) for line in warehouse_map
]
warehouse_map_part2_dict = defaultdict(
    lambda: defaultdict(lambda: "!"),
    enumerate(
        defaultdict((lambda: "!"), enumerate(line)) for line in warehouse_map_part2
    ),
)
rows_part2 = len(warehouse_map_part2)
cols_part2 = len(warehouse_map_part2[0])

directions = [(0, 1), (0, -1), (-1, 0), (1, 0)]
characters = [">", "<", "^", "v"]
character_direction_dict = dict(zip(characters, directions))


# Helper functions
def move(drow, dcol, row, col):
    if warehouse_map_dict[row][col] == "#":
        # Hit a wall
        return False
    elif warehouse_map_dict[row][col] == ".":
        return True
    else:
        # Check recursively if we can move the box
        if move(drow, dcol, row + drow, col + dcol):
            # You can move the box
            warehouse_map_dict[row + drow][col + dcol] = warehouse_map_dict[row][col]
            warehouse_map_dict[row][col] = "."
            return True
        return False


## Part 1
@timeit
def part1():
    # Find robot starting position
    robot_row, robot_col = 0, 0
    for row in range(rows):
        for col in range(cols):
            if warehouse_map_dict[row][col] == "@":
                robot_row, robot_col = row, col

    # Begin movements
    for movement in movements:
        drow, dcol = character_direction_dict[movement]
        if move(drow, dcol, robot_row, robot_col):
            robot_row, robot_col = robot_row + drow, robot_col + dcol

    # Sum of GPS coordinates
    # The GPS coordinate of a box is equal to 100 times its distance
    # from the top edge of the map plus its distance from the left edge of the map.
    return sum(
        100 * row + col
        for row in range(rows)
        for col in range(cols)
        if warehouse_map_dict[row][col] == "O"
    )


print(part1())


# Helper functions for Part 2
def check_valid_move(drow, dcol, row, col, already_checked):
    if (row, col) in already_checked:
        return already_checked[(row, col)]
    already_checked[(row, col)] = True
    if warehouse_map_part2_dict[row][col] == "#":
        already_checked[(row, col)] = False
    elif warehouse_map_part2_dict[row][col] == ".":
        already_checked[(row, col)] = True
    elif warehouse_map_part2_dict[row][col] == "@":
        already_checked[(row, col)] = check_valid_move(
            drow, dcol, row + drow, col + dcol, already_checked
        )
    elif warehouse_map_part2_dict[row][col] == "[":
        already_checked[(row, col)] = check_valid_move(
            drow, dcol, row + drow, col + dcol, already_checked
        ) and check_valid_move(drow, dcol, row, col + 1, already_checked)
    elif warehouse_map_part2_dict[row][col] == "]":
        already_checked[(row, col)] = check_valid_move(
            drow, dcol, row + drow, col + dcol, already_checked
        ) and check_valid_move(drow, dcol, row, col - 1, already_checked)
    return already_checked[(row, col)]


def move_robot(drow, dcol, row, col, already_committed):
    if (row, col) in already_committed:
        return
    already_committed.add((row, col))
    if warehouse_map_part2_dict[row][col] == "#":
        return
    elif warehouse_map_part2_dict[row][col] == ".":
        return
    elif warehouse_map_part2_dict[row][col] == "@":
        move_robot(drow, dcol, row + drow, col + dcol, already_committed)
        warehouse_map_part2_dict[row + drow][col + dcol] = warehouse_map_part2_dict[
            row
        ][col]
        warehouse_map_part2_dict[row][col] = "."
    elif warehouse_map_part2_dict[row][col] == "[":
        move_robot(drow, dcol, row + drow, col + dcol, already_committed)
        move_robot(drow, dcol, row, col + 1, already_committed)
        warehouse_map_part2_dict[row + drow][col + dcol] = warehouse_map_part2_dict[
            row
        ][col]
        warehouse_map_part2_dict[row][col] = "."
    elif warehouse_map_part2_dict[row][col] == "]":
        move_robot(drow, dcol, row + drow, col + dcol, already_committed)
        move_robot(drow, dcol, row, col - 1, already_committed)
        warehouse_map_part2_dict[row + drow][col + dcol] = warehouse_map_part2_dict[
            row
        ][col]
        warehouse_map_part2_dict[row][col] = "."


## Part 2
@timeit
def part2():
    # Find robot starting position
    robot_row, robot_col = 0, 0
    for row in range(rows_part2):
        for col in range(cols_part2):
            if warehouse_map_part2_dict[row][col] == "@":
                robot_row, robot_col = row, col

    # Begin movements
    for movement in movements:
        drow, dcol = character_direction_dict[movement]
        if check_valid_move(drow, dcol, robot_row, robot_col, dict()):
            move_robot(drow, dcol, robot_row, robot_col, set())
            robot_row, robot_col = robot_row + drow, robot_col + dcol

    # Sum of GPS coordinates
    # For these larger boxes, distances are measured from the edge
    # of the map to the closest edge of the box in question.
    return sum(
        100 * row + col
        for row in range(rows_part2)
        for col in range(cols_part2)
        if warehouse_map_part2_dict[row][col] == "["
    )


print(part2())
