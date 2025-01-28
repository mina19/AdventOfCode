## Pull Data
from collections import defaultdict
from pathlib import Path

from get_data import save_data, timeit

save_data(2024, day := 23)
data = Path(f"2024/{day}/day{day:02d}.txt").read_text().splitlines()
# data = Path(f"2024/{day}/day{day:02d}_sample.txt").read_text().splitlines()

network_pairs = [line.split('-') for line in data]
graph = defaultdict(set)
computers = set()

# Parse the input pairs and build the graph
for comp1, comp2 in network_pairs:
    graph[comp1].add(comp2)
    graph[comp2].add(comp1)
    computers.add(comp1)
    computers.add(comp2)

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
def find_max_clique():
    def is_clique(nodes):
        """Check if the given set of nodes forms a clique"""
        for node in nodes:
            # For each node, check if it's connected to all other nodes
            if not all(other_node in graph[node] for other_node in nodes if other_node != node):
                return False
        return True
    
    def find_all_cliques(current_clique, remaining):
        """Recursively find all possible cliques"""
        if not remaining:
            if is_clique(current_clique):
                return [current_clique]
            return []
        
        # Track the cliques found
        cliques = []
        current_node = remaining[0]

        # Try including the current node
        new_clique = current_clique | {current_node}
        if is_clique(new_clique):
            cliques.extend(find_all_cliques(new_clique, 
                                         [node for node in remaining[1:] 
                                          if node in graph[current_node]]))
        
        # Try excluding the current node
        cliques.extend(find_all_cliques(current_clique, remaining[1:]))
        
        return cliques

    # Start with empty clique and all nodes as candidates
    all_cliques = find_all_cliques(set(), list(computers))
    
    # Return the largest clique found
    if not all_cliques:
        return set()
    
    return ','.join(sorted(max(all_cliques, key=len)))

print(find_max_clique())