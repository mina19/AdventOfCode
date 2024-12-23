## Pull Data
from collections import defaultdict
from itertools import combinations
from pathlib import Path

from get_data import save_data, timeit

save_data(2024, day := 23)
data = Path(f"2024/{day}/day{day:02d}.txt").read_text().splitlines()
# data = Path(f"2024/{day}/day{day:02d}_sample.txt").read_text().splitlines()

network_pairs = [line.split('-') for line in data]

# All computers in network:
computers = list(set( [item for sublist in network_pairs for item in sublist]))
computers_start_t = [comp for comp in computers if comp.startswith('t')]

## Part 1
@timeit
def part1():
    solutions = []
    networks_with_computers_start_t = [pair for pair in network_pairs if any(computer in computers_start_t for computer in pair)]
    for network in networks_with_computers_start_t:
        (other_comp, t_comp) = (network[1], network[0]) if network[0].startswith('t') else (network[0], network[1])
        networks_with_other_comp = [pair for pair in network_pairs if other_comp in pair]
        for network in networks_with_other_comp:
            third_comp = network[1] if network[0] == other_comp else network[0]
            if [third_comp, t_comp] in network_pairs or [t_comp, third_comp] in network_pairs:
                if set([third_comp, other_comp, t_comp]) not in solutions:
                    solutions.append(set([third_comp, other_comp, t_comp]))
    return len(solutions)


print(part1())


## Part 2
@timeit
def part2():
    pass


part2()
