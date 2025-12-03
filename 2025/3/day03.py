## Pull Data
from pathlib import Path

from get_data import save_data, timeit

save_data(year := 2025, day := 3)
data = Path(f"{year}/{day}/day{day:02d}.txt").read_text()
data = Path(f"{year}/{day}/day{day:02d}_sample.txt").read_text()


## Part 1
@timeit
def part1():
    lines = data.splitlines()

    result = 0
    for line in lines:
        joltage = 0
        for i in range(len(line)):
            for j in range(i + 1, len(line)):
                current = int(line[i] + line[j])
                if current > joltage:
                    joltage = current
        result += joltage

    return result


print(part1())


## Part 2
@timeit
def part2():
    lines = data.splitlines()

    result = 0
    for line in lines:
        # Example for line '987654321111111'
        # [['9', '9', '9', '9', '9', '9', '9', '9', '9', '9', '9', '9'],
        #  ['8', '98', '98', '98', '98', '98', '98', '98', '98', '98', '98', '98'],
        #  ['7', '97', '987', '987', '987', '987', '987', '987', '987', '987', '987', '987'],
        #  ['6', '96', '986', '9876', '9876', '9876', '9876', '9876', '9876', '9876', '9876', '9876'],
        #  ['5', '95', '985', '9875', '98765', '98765', '98765', '98765', '98765', '98765', '98765', '98765'],
        #  ['4', '94', '984', '9874', '98764', '987654', '987654', '987654', '987654', '987654', '987654', '987654'],
        #  ['3', '93', '983', '9873', '98763', '987653', '9876543', '9876543', '9876543', '9876543', '9876543', '9876543'],
        #  ['2', '92', '982', '9872', '98762', '987652', '9876542', '98765432', '98765432', '98765432', '98765432', '98765432'],
        #  ['1', '91', '981', '9871', '98761', '987651', '9876541', '98765431', '987654321', '987654321', '987654321', '987654321'],
        #  ['1', '91', '981', '9871', '98761', '987651', '9876541', '98765431', '987654321', '9876543211', '9876543211', '9876543211'],
        #  ['1', '91', '981', '9871', '98761', '987651', '9876541', '98765431', '987654321', '9876543211', '98765432111', '98765432111'],
        #  ['1', '91', '981', '9871', '98761', '987651', '9876541', '98765431', '987654321', '9876543211', '98765432111', '987654321111'],
        #  ['1', '91', '981', '9871', '98761', '987651', '9876541', '98765431', '987654321', '9876543211', '98765432111', '987654321111'],
        #  ['1', '91', '981', '9871', '98761', '987651', '9876541', '98765431', '987654321', '9876543211', '98765432111', '987654321111'],
        #  ['1', '91', '981', '9871', '98761', '987651', '9876541', '98765431', '987654321', '9876543211', '98765432111', '987654321111']]

        # Create DP table for storing best numbers where dp[i][j] is the best number ending with line[i] using j+1 digits or less
        dp = [["" for i in range(12)] for j in range(len(line))]
        joltage = 0

        for i in range(len(line)):
            dp[i][0] = line[i]
            # Try to build numbers of length 2 to 12 ending at position i
            for j in range(1, 12):
                accumulator = ""
                # Look back at all previous positions to find the best number of length j
                for k in range(0, i):
                    current = dp[k][j - 1]
                    # If curr is not empty and is greater than accumulator, update accumulator
                    if current != "" and (
                        accumulator == "" or int(current) > int(accumulator)
                    ):
                        accumulator = current
                    if current == "":
                        print("debug")
                # Build the new number by appending the current digit
                dp[i][j] = accumulator + line[i]
            # After filling dp for this position, check if we have a new max for 12 digits
            joltage = max(joltage, int(dp[i][11]))
        # Add the largest 12-digit number for this line to the result
        result += joltage

    return result


print(part2())
