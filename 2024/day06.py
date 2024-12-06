## Pull Data
from pathlib import Path
from collections import defaultdict

from get_data import save_data, timeit

save_data(2024, day := 6)
data = Path(f"day{day:02d}.txt").read_text().splitlines()
data = Path(f"2024/day{day:02d}_sample.txt").read_text().splitlines()

# Hash the data. If we hit boundary return a !
data_dict = defaultdict(
    (lambda: defaultdict(lambda: "!")),
    enumerate(defaultdict((lambda: "!"), enumerate(line)) for line in data),
)


## Part 1
@timeit
def part1():
    # Lazy way to find the coordinates of ^
    i = 0
    j = 0
    for row in range(len(data)):
        for col in range(len(data[0])):
            if data_dict[row][col] == "^":
                i = row
                j = col

    # Begin traversing the grid/dictionary
    result = 0
    current = (-1, 0)  # Starting direction North
    while data_dict[i][j] != "!":  # Continue until hitting boundary
        # Mark current position as visited
        if data_dict[i][j] != "X":
            data_dict[i][j] = "X"
            result += 1

        # If hitting a wall (#), rotate direction right
        if data_dict[i + current[0]][j + current[1]] == "#":
            current = (current[1], -current[0])
        else:
            # Move in current direction
            i += current[0]
            j += current[1]
    return result


print(part1())

## Part 2


@timeit
def part2():
    pass


part2()
