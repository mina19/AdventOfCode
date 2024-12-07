## Pull Data
from pathlib import Path

from get_data import save_data, timeit

save_data(2024, day := 7)
data = Path(f"2024/7/day{day:02d}.txt").read_text().splitlines()
data = Path(f"2024/7/day{day:02d}_sample.txt").read_text().splitlines()

outputs = [int(line.split(":")[0]) for line in data]
inputs = [[int(num) for num in line.split(":")[1].split()] for line in data]


# Helper functions
def all_combinations(input, concat=False):
    # Create all possible results of * and + and concatenation if concat is True
    # Operators are always evaluated left-to-right, not according to precedence rules.

    if len(input) == 1:
        # Recursive stopping point
        return set([input[0]])

    all_results = set()

    # Take all numbers but the first one
    sub_combinations = all_combinations(input[1:], concat=concat)

    # Calculate multiplications and additions
    all_results.update(input[0] + x for x in sub_combinations)
    all_results.update(input[0] * x for x in sub_combinations)
    # If concatenation for Part 2:
    if concat:
        all_results.update(int(str(x) + str(input[0])) for x in sub_combinations)

    return all_results


# Memoizing should make it a bit faster
# It actually performs worse with concatenation...
def all_combinations_memoized(input, memo=None, concat=False):
    # Create all possible results of * and + and concatenation if concat is True
    # Operators are always evaluated left-to-right, not according to precedence rules.

    # Example:
    # all_combinations_memoized([81, 40, 27][::-1], concat=True)
    # all_combinations_memoized([27, 40, 81], concat=True)
    # (81,) {81}
    # (40, 81) {
    #     121 = 81 + 40,
    #     3240 = 81 * 40,
    #     8140 = 81 || 40
    # }
    # Returns: {
    #     148 = (81 + 40) + 27,
    #     3267 = (81 + 40) * 27,
    #     12127 = (81 + 40) || 27,
    #     3267 = (81 * 40) + 27, (this is a repeat)
    #     87480 = (81 * 40) * 27,
    #     324027 = (81 * 40) || 27,
    #     8167 = (81 || 40) + 27,
    #     219780 = (81 || 40) * 27,
    #     814027 = (81 || 40) || 27,
    # }

    # Initialize memo dictionary if not provided
    if memo is None:
        memo = {}

    # Convert input to tuple so it can be used as dictionary key
    input_key = tuple(input)

    # If we've already calculated this combination, return it
    if input_key in memo:
        return memo[input_key]

    # Base case: single number
    if len(input) == 1:
        # Save like this: memo[(input[0],)] = {input[0]}
        memo[input_key] = set([input[0]])
        return memo[input_key]

    all_results = set()

    # Get sub-combinations (memoized)
    # Take all numbers but the first one
    sub_combinations = all_combinations_memoized(input[1:], memo, concat=concat)

    # Calculate multiplications and additions
    all_results.update(input[0] + x for x in sub_combinations)
    all_results.update(input[0] * x for x in sub_combinations)
    # If concatenation for Part 2:
    if concat:
        all_results.update(int(str(x) + str(input[0])) for x in sub_combinations)

    # Store result in memo before returning
    memo[input_key] = all_results
    return all_results


## Part 1
@timeit
def part1():
    return sum(
        [
            output
            for input, output in zip(inputs, outputs)
            if output in all_combinations(input[::-1])
        ]
    )


@timeit
def part1_memoized():
    return sum(
        [
            output
            for input, output in zip(inputs, outputs)
            if output in all_combinations_memoized(input[::-1])
        ]
    )


print(part1())
print(part1_memoized())


## Part 2
# Concatenation....
@timeit
def part2():
    return sum(
        [
            output
            for input, output in zip(inputs, outputs)
            if output in all_combinations(input[::-1], concat=True)
        ]
    )


@timeit
def part2_memoized():
    return sum(
        [
            output
            for input, output in zip(inputs, outputs)
            if output in all_combinations_memoized(input[::-1], concat=True)
        ]
    )


print(part2())
print(part2_memoized())
