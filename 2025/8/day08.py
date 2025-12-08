## Pull Data
import math
import operator
from functools import reduce
from pathlib import Path

import networkx as nx

from get_data import save_data, timeit

save_data(year := 2025, day := 8)
data = Path(f"{year}/{day}/day{day:02d}.txt").read_text()
# data = Path(f"{year}/{day}/day{day:02d}_sample.txt").read_text()


## Part 1
@timeit
def part1():
    coords = [tuple(map(int, line.split(","))) for line in data.splitlines()]

    all_edges = [
        (idx1, idx2, math.dist(coord_idx1, coord_idx2))
        for idx1, coord_idx1 in enumerate(coords)
        for idx2, coord_idx2 in enumerate(coords[idx1 + 1 :], start=idx1 + 1)
    ]

    all_edges.sort(key=lambda x: x[2])

    # Create an empty undirected graph
    G = nx.Graph()

    for node1, node2, distance in all_edges[:1000]:
        G.add_edge(node1, node2, weight=distance)

    # Get all connected components (sorted by size, largest first)
    connected_components = sorted(nx.connected_components(G), key=len, reverse=True)
    top3_circuits = connected_components[:3]

    return reduce(operator.mul, [len(c) for c in top3_circuits])


print(part1())


## Part 2
@timeit
def part2():
    coords = [tuple(map(int, line.split(","))) for line in data.splitlines()]

    all_edges = [
        (idx1, idx2, math.dist(coord_idx1, coord_idx2))
        for idx1, coord_idx1 in enumerate(coords)
        for idx2, coord_idx2 in enumerate(coords[idx1 + 1 :], start=idx1 + 1)
    ]

    all_edges.sort(key=lambda x: x[2])

    # Create an empty undirected graph
    G = nx.Graph()

    while True:
        for node1, node2, distance in all_edges:
            G.add_edge(node1, node2, weight=distance)

            # Get all connected components (sorted by size, largest first)
            connected_components = sorted(
                nx.connected_components(G), key=len, reverse=True
            )
            if len(connected_components) == 1 and len(connected_components[0]) == len(
                coords
            ):
                coord1 = coords[node1]
                coord2 = coords[node2]
                break

        return coord1[0] * coord2[0]


print(part2())
