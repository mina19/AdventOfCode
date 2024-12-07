## Pull Data
from pathlib import Path

from get_data import save_data, timeit

save_data(2024, day := 7)
data = Path(f"2024/7/day{day:02d}.txt").read_text().splitlines()
# data = Path(f"2024/7/day{day:02d}_sample.txt").read_text().splitlines()
outputs = [int(line.split(":")[0]) for line in data]
inputs = [[int(num) for num in line.split(":")[1].split()] for line in data]


# Helper function
def all_combinations(nums):
    # Create all possible results of * and +
    if len(nums) == 1:
        # Recursive stopping point
        return set([nums[0]])

    all_results = set()

    # Take all numbers but the first one
    # This means all numbers but the last number in original list
    sub_combinations = all_combinations(nums[1:])

    # Calculate multiplications and additions
    all_results.update(nums[0] * x for x in sub_combinations)
    all_results.update(nums[0] + x for x in sub_combinations)

    return all_results


# Memoizing should make it a bit faster
def all_combinations_memoized(nums, memo=None):
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
    sub_combinations = all_combinations_memoized(nums[1:], memo)

    # Calculate multiplications and additions
    all_results.update(nums[0] * x for x in sub_combinations)
    all_results.update(nums[0] + x for x in sub_combinations)

    # Store result in memo before returning
    memo[nums_key] = all_results
    return all_results


## Part 1
@timeit
def part1():
    result = 0
    for input, output in zip(inputs, outputs):
        all_results = all_combinations(input[::-1])
        if output in all_results:
            result += output
    return result


@timeit
def part1_memoized():
    result = 0
    for input, output in zip(inputs, outputs):
        all_results = all_combinations_memoized(input[::-1])
        if output in all_results:
            result += output
    return result


print(part1())
print(part1_memoized())


## Part 2
@timeit
def part2():
    pass


part2()
