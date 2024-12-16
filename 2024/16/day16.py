## Pull Data
from pathlib import Path
from collections import defaultdict, deque
from heapq import heappush, heappop
from itertools import chain

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
def part1_heap():
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


@timeit
def solve_bfs():
    # Find start and end positions
    for row in range(rows):
        for col in range(cols):
            if data_dict[row][col] == "S":
                start_position = (row, col)
            elif data_dict[row][col] == "E":
                end_position = (row, col)

    queue = deque([(0, (start_position, 0), [start_position])])
    visited = {}  # Track state:score instead of just states
    paths = []  # Store successful paths
    scores = []
    while queue:
        current_score, (current_position, current_direction_index), current_path = (
            queue.popleft()
        )

        state = (current_position, current_direction_index)
        # Only skip if we've seen this state with a better score
        if state in visited and visited[state] <= current_score:
            continue

        # Keep track of current position and current direction
        visited[state] = current_score

        if data_dict[current_position[0]][current_position[1]] == "#":
            continue
        if current_position == end_position:
            scores.append(current_score)
            paths.append(current_path)  # Save successful path
            continue

        # Move forward in current facing direction
        drow, dcol = directions[current_direction_index]
        new_pos = (current_position[0] + drow, current_position[1] + dcol)
        # Check boundaries before adding new position
        if 0 <= new_pos[0] < rows and 0 <= new_pos[1] < cols:
            # Add new_pos to path history
            new_path = current_path + [new_pos]
            queue.append(
                (
                    current_score + 1,
                    (
                        new_pos,
                        current_direction_index,
                    ),
                    new_path,
                ),
            )

        # Reindeer can also rotate clockwise or counterclockwise 90 degrees
        # at a time (increasing their score by 1000 points).
        for turn_type in ["right", "left"]:
            new_direction_index = rotate_direction(current_direction_index, turn_type)
            queue.append(
                (
                    current_score + 1000,
                    (current_position, new_direction_index),
                    current_path,
                ),
            )

    # Which tiles are part of any best path through the maze
    min_score = min(scores)
    tile_count = len(list(chain(*paths))) - (len(paths) - 1) * 2

    return min_score, tile_count


print(part1_heap())

## Part 2
# Heap solution will not work for this part. Need to track all the unique paths that give same best score.
# Use BFS solution

print(solve_bfs())
