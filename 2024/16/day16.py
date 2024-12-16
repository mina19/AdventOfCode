## Pull Data
from pathlib import Path
from collections import defaultdict
from heapq import heappush, heappop

from get_data import save_data, timeit

save_data(2024, day := 16)
data = Path(f"2024/{day}/day{day:02d}.txt").read_text().splitlines()
# data = Path(f"2024/{day}/day{day:02d}_sample.txt").read_text().splitlines()

data_dict = defaultdict(
    lambda: defaultdict(lambda: "!"),
    enumerate(defaultdict((lambda: "!"), enumerate(line)) for line in data),
)

rows = len(data)
cols = len(data[0])

directions = [(0, 1), (-1, 0), (0, -1), (1, 0)]  # right, up, left, down


# Helper function
def rotate_direction(current_direction_index, turn_type):
    if turn_type == "left":
        return (current_direction_index + 1) % 4
    return (current_direction_index - 1) % 4


## Part 1
@timeit
def part1():
    # Find start and end positions
    for row in range(rows):
        for col in range(cols):
            if data_dict[row][col] == "S":
                start_position = (row, col)
            elif data_dict[row][col] == "E":
                end_position = (row, col)

    priority_queue = [(0, (start_position, 0))]
    visited = set()
    score = 0
    while priority_queue:
        current_score, (current_position, current_direction_index) = heappop(
            priority_queue
        )
        if (current_position, current_direction_index) in visited:
            continue

        # Keep track of current position and current direction
        visited.add((current_position, current_direction_index))

        if data_dict[current_position[0]][current_position[1]] == "#":
            continue
        if current_position == end_position:
            score = current_score
            break

        # Move forward in current facing direction
        drow, dcol = directions[current_direction_index]
        heappush(
            priority_queue,
            (
                current_score + 1,
                (
                    (
                        current_position[0] + drow,
                        current_position[1] + dcol,
                    ),
                    current_direction_index,
                ),
            ),
        )

        # Reindeer can also rotate clockwise or counterclockwise 90 degrees
        # at a time (increasing their score by 1000 points).
        for turn_type in ["right", "left"]:
            new_direction_index = rotate_direction(current_direction_index, turn_type)
            heappush(
                priority_queue,
                (current_score + 1000, (current_position, new_direction_index)),
            )

    return score


print(part1())


## Part 2
@timeit
def part2():
    pass


part2()
