## Pull Data
from pathlib import Path

from get_data import save_data, timeit

save_data(2024, day := 7)
data = Path(f"2024/7/day{day:02d}.txt").read_text().splitlines()
# data = Path(f"2024/7/day{day:02d}_sample.txt").read_text().splitlines()
outputs = [int(line.split(":")[0]) for line in data]
inputs = [[int(num) for num in line.split(":")[1].split()] for line in data]


# Helper function
def all_combinations(nums, concat=False):
    # Create all possible results of * and +
    if len(nums) == 1:
        # Recursive stopping point
        return set([nums[0]])

    all_results = set()

    # Take all numbers but the first one
    # This means all numbers but the last number in original list
    sub_combinations = all_combinations(nums[1:], concat=concat)

    # Calculate multiplications and additions
    all_results.update(nums[0] * x for x in sub_combinations)
    all_results.update(nums[0] + x for x in sub_combinations)
    # If concatenation for Part 2:
    if concat:
        all_results.update(int(str(x) + str(nums[0])) for x in sub_combinations)

    return all_results


# Memoizing should make it a bit faster
# It actually performs worse with concatenation...
def all_combinations_memoized(nums, memo=None, concat=False):
    # Create all possible results of * and + using memoization

    # Initialize memo dictionary if not provided
    if memo is None:
        memo = {}

    # Convert nums to tuple so it can be used as dictionary key
    nums_key = tuple(nums)

    # If we've already calculated this combination, return it
    if nums_key in memo:
        return memo[nums_key]

    # Base case: single number
    if len(nums) == 1:
        # Save like this: memo[(nums[0],)] = {nums[0]}
        memo[nums_key] = set([nums[0]])
        return memo[nums_key]

    all_results = set()

    # Get sub-combinations (memoized)
    sub_combinations = all_combinations_memoized(nums[1:], memo, concat=concat)

    # Calculate multiplications and additions
    all_results.update(nums[0] * x for x in sub_combinations)
    all_results.update(nums[0] + x for x in sub_combinations)
    # If concatenation for Part 2:
    if concat:
        all_results.update(int(str(x) + str(nums[0])) for x in sub_combinations)

    # Store result in memo before returning
    memo[nums_key] = all_results
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
