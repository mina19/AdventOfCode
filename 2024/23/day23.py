## Pull Data
from pathlib import Path

from get_data import save_data, timeit

save_data(2024, day := 23)
data = Path(f"2024/{day}/day{day:02d}.txt").read_text().splitlines()
# data = Path(f"2024/{day}/day{day:02d}_sample.txt").read_text().splitlines()

network_pairs = [line.split('-') for line in data]

# Get all unique computers
all_computers = set()
for comp1, comp2 in network_pairs:
    all_computers.add(comp1)
    all_computers.add(comp2)

## Part 1
@timeit
def part1():
   # Find networks that have at least one computer starting with 't'
   t_networks = [pair for pair in network_pairs 
                if any(computer.startswith('t') for computer in pair)]
   
   solutions = []
   for network in t_networks:
       # Identify t_comp and other_comp from the pair
       t_comp = next(comp for comp in network if comp.startswith('t'))
       other_comp = next(comp for comp in network if comp != t_comp)
       
       # Find all networks containing other_comp
       connected_networks = [pair for pair in network_pairs if other_comp in pair]
       
       # For each network connected to other_comp
       for connected_network in connected_networks:
           # Find the third computer
           third_comp = next(comp for comp in connected_network if comp != other_comp)
           
           # Check if third_comp is also connected to t_comp
           if [third_comp, t_comp] in network_pairs or [t_comp, third_comp] in network_pairs:
               # Add the trio to solutions if not already present
               trio = {third_comp, other_comp, t_comp}
               if trio not in solutions:
                   solutions.append(trio)
   
   return len(solutions)


print(part1())


## Part 2
@timeit
def part2():
    pass

print(part2())
