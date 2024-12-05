## Pull Data
from pathlib import Path

from get_data import save_data, timeit

save_data(2024, day := 5)
data = Path(f"day{day:02d}.txt").read_text().splitlines()
# data = Path(f"2024/day{day:02d}_sample.txt").read_text().splitlines()

rules = [line.split("|") for line in data if "|" in line]
rules = [[int(x) for x in sublist] for sublist in rules]
updates = [line.split(",") for line in data if "," in line]
updates = [[int(x) for x in sublist] for sublist in updates]


## Part 1
def check_update(update):
    result = True
    for rule in rules:
        if rule[0] in update and rule[1] in update:
            ind1 = update.index(rule[0])
            ind2 = update.index(rule[1])
            if ind1 > ind2:
                result = False

    return result


@timeit
def part1():
    total = 0
    for update in updates:
        if check_update(update):
            total += update[len(update) // 2]

    return total


print(part1())
## Part 2


def fix_update(update):
    relevant_rules = []
    for rule in rules:
        if rule[0] in update and rule[1] in update:
            relevant_rules.append(rule)

    def find_last(rules, update):
        front_numbers = [rule[0] for rule in rules]
        num = list(set(update).difference(front_numbers))[0]
        return num

    # Construct half correct update
    new_update = []
    while len(new_update) < len(update):
        last_num = find_last(relevant_rules, update)
        # Find which rule has last_num in the last position
        useless_rules = [rule for rule in relevant_rules if rule[1] == last_num]
        for useless_rule in useless_rules:
            relevant_rules.remove(useless_rule)
        update.remove(last_num)
        new_update.insert(0, last_num)

    return new_update


@timeit
def part2():
    result = []
    for update in updates:
        if not check_update(update):
            result.append(fix_update(update))
    return sum([item[0] for item in result])


print(part2())
