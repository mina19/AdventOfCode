## Pull Data
from functools import cache
from pathlib import Path

from get_data import save_data, timeit

save_data(2024, day := 19)
data = Path(f"2024/{day}/day{day:02d}.txt").read_text()
# data = Path(f"2024/{day}/day{day:02d}_sample.txt").read_text()

available_patterns = data.split("\n\n")[0].split(", ")
desired_patterns = data.split("\n\n")[1].splitlines()


# Helper functions
def can_do_memo(pattern, memo):
    # Initialize memo dict on first call
    if memo is None:
        memo = {}

    # Return memoized result if available
    if pattern in memo:
        return memo[pattern]

    if pattern == "":
        return True

    for candidate in available_patterns:
        if pattern.startswith(candidate):
            if can_do_memo(pattern[len(candidate) :], memo):
                memo[pattern] = True
                return True

    memo[pattern] = False
    return False


@cache
def can_do(pattern):
    if pattern == "":
        return True

    for candidate in available_patterns:
        if pattern.startswith(candidate):
            if can_do(pattern[len(candidate) :]):
                return True

    return False


def count_ways_memo(pattern, memo):
    """
    brwrr -> candidate b  -> rwrr
    rwrr  -> candidate r  -> wrr
    wrr   -> candidate wr -> r
    r     -> candidate r  -> ""

    memo: {'r': 1}
    memo: {'r': 1, 'wrr': 1}
    memo: {'r': 1, 'wrr': 1, 'rwrr': 1}

    brwrr -> candidate br  -> wrr # Already in memo!

    memo: {'r': 1, 'wrr': 1, 'rwrr': 1, 'brwrr': 2}
    """
    # Initialize memo dict on first call
    if memo is None:
        memo = {}

    # Return memoized result if available
    if pattern in memo:
        return memo[pattern]

    if pattern == "":
        return 1

    ways = 0
    for candidate in available_patterns:
        if pattern.startswith(candidate):
            ways += count_ways_memo(pattern[len(candidate) :], memo)

    memo[pattern] = ways
    return ways


@cache
def count_ways(pattern):
    if pattern == "":
        return 1

    ways = 0
    for candidate in available_patterns:
        if pattern.startswith(candidate):
            ways += count_ways(pattern[len(candidate) :])
    return ways


@cache
def pattern_solver(pattern, mode="can_do"):
    if pattern == "":
        return True if mode == "can_do" else 1

    if mode == "can_do":
        for candidate in available_patterns:
            if pattern.startswith(candidate):
                if pattern_solver(pattern[len(candidate) :], mode="can_do"):
                    return True
        return False
    else:  # count_ways mode
        ways = 0
        for candidate in available_patterns:
            if pattern.startswith(candidate):
                ways += pattern_solver(pattern[len(candidate) :], mode="count_ways")
        return ways


## Part 1
@timeit
def part1():
    return sum(map(lambda pattern: pattern_solver(pattern, "can_do"), desired_patterns))


print(part1())


## Part 2
@timeit
def part2():
    return sum(
        map(lambda pattern: pattern_solver(pattern, "count_ways"), desired_patterns)
    )


print(part2())
