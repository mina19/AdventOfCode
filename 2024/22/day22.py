## Pull Data
from pathlib import Path

from get_data import save_data, timeit

save_data(2024, day := 22)
data = Path(f"2024/{day}/day{day:02d}.txt").read_text().splitlines()
# data = Path(f"2024/{day}/day{day:02d}_sample.txt").read_text().splitlines()

# Helper functions
def mix(s, num):
    """
    To mix a value into the secret number, calculate 
    the bitwise XOR of the given value and the secret number.
    """
    return s ^ num

def prune(s):
    """
    To prune the secret number, calculate the value of the
    secret number modulo 16777216.
    """
    return s % 16777216

def iterate(s):
    # Calculate the result of multiplying the secret number by 64.
    # Then, mix this result into the secret number.
    # Finally, prune the secret number.
    s = prune(mix(s, s * 64))

    # Calculate the result of dividing the secret number by 32.
    # Round the result down to the nearest integer.
    # Then, mix this result into the secret number.
    # Finally, prune the secret number.
    s = prune(mix(s, s // 32))

    # Calculate the result of multiplying the secret number by 2048.
    # Then, mix this result into the secret number.
    # Finally, prune the secret number.
    s = prune(mix(s, s * 2048))

    return s
    
## Part 1
@timeit
def part1():
    result = 0
    for line in data:
        secret_number = int(line)
        for _ in range(2000):
            secret_number = iterate(secret_number)
        result += secret_number

    return result


print(part1())


## Part 2
@timeit
def part2():
    pass


part2()
