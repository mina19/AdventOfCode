## Pull Data
from pathlib import Path
from collections import defaultdict

from get_data import save_data, timeit

save_data(2024, day := 15)
data = Path(f"2024/{day}/day{day:02d}.txt").read_text()
data = Path(f"2024/{day}/day{day:02d}_sample.txt").read_text()

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


## Part 2
@timeit
def part2():
    pass


part2()
