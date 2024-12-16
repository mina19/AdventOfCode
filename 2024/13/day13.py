## Pull Data
from pathlib import Path
import re
from get_data import save_data, timeit
from heapq import heappop, heappush

save_data(2024, day := 13)
data = Path(f"2024/{day}/day{day:02d}.txt").read_text()
# data = Path(f"2024/{day}/day{day:02d}_sample.txt").read_text()

# Group into data for each claw
claws = [lines.split("\n") for lines in data.split("\n\n")]

pattern = r"(.*): X[+=](\d+), Y[+=](\d+)"


def find_combo(line):
    match = re.match(pattern, line)
    return int(match[2]), int(match[3])


## Part 1
@timeit
def part1_heap():
    tokens = 0
    for claw in claws:
        # Get moves for each button and prize
        a_x, a_y = find_combo(claw[0])
        b_x, b_y = find_combo(claw[1])
        prize_x, prize_y = find_combo(claw[2])

        # Track positions to visit using priority queue
        priority_queue = [(0, 0, 0)]  # (token cost, x, y)
        visited = set()  # Track visited positions

        while priority_queue:
            # Pop the position with smallest cost
            current_tokens, current_x, current_y = heappop(priority_queue)

            # Skip if we've already visited this position
            if (current_x, current_y) in visited:
                continue

            # Mark position as visited
            visited.add((current_x, current_y))

            # Check if we've reached the prize
            if current_x == prize_x and current_y == prize_y:
                tokens += current_tokens
                break
            # Only continue if we're not past the prize
            elif current_x <= prize_x and current_y <= prize_y:
                # Add both possible moves to queue with their costs
                # It costs 3 tokens to push the A button and 1 token to push the B button
                heappush(
                    priority_queue,
                    (current_tokens + 3, current_x + a_x, current_y + a_y),
                )
                heappush(
                    priority_queue,
                    (current_tokens + 1, current_x + b_x, current_y + b_y),
                )

    return tokens


print(part1_heap())


## Part 2
@timeit
def solve(part2=False):
    tokens = 0
    for claw in claws:
        # Get moves for each button and prize
        a_x, a_y = find_combo(claw[0])
        b_x, b_y = find_combo(claw[1])
        prize_x, prize_y = find_combo(claw[2])
        if part2:
            prize_x += 10_000_000_000_000
            prize_y += 10_000_000_000_000

        # Matrix solution
        sol_x = (b_y * prize_x - b_x * prize_y) / (a_x * b_y - b_x * a_y)
        sol_y = (-a_y * prize_x + a_x * prize_y) / (a_x * b_y - b_x * a_y)

        if sol_x.is_integer() and sol_y.is_integer():
            tokens += 3 * sol_x + sol_y

    return tokens


print(solve())

print(solve(part2=True))
