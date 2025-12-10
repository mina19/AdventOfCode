from itertools import product
from pathlib import Path

import numpy as np
from scipy.optimize import (
    Bounds,
    LinearConstraint,
    linprog,
    milp,
)

from get_data import save_data, timeit

save_data(year := 2025, day := 10)
data = Path(f"{year}/{day}/day{day:02d}.txt").read_text().splitlines()
# data = Path(f"{year}/{day}/day{day:02d}_sample.txt").read_text().splitlines()

split_data = [line.split(" ") for line in data]

diagrams = []
indicator_diagrams = [item[0].replace("[", "").replace("]", "") for item in split_data]
for diagram in indicator_diagrams:
    converted_diagram = []
    for char in diagram:
        if char == "#":
            converted_diagram.append(1)
        else:
            converted_diagram.append(0)
    diagrams.append(np.array(converted_diagram))

button_schematics = []
button_wiring_schematics = [item[1:-1] for item in split_data]
for diagram, schematic in zip(diagrams, button_wiring_schematics):
    n = len(diagram)
    buttons = []
    for item in schematic:
        button = list(map(int, item.replace("(", "").replace(")", "").split(",")))
        default_state = np.zeros(n, dtype=int)
        for i in button:
            default_state[i] = 1
        buttons.append(default_state)
    button_schematics.append(buttons)

joltages = [item[-1] for item in split_data]
joltages = [
    np.array(list(map(int, item.replace("{", "").replace("}", "").split(","))))
    for item in joltages
]


## Part 1
@timeit
def part1():
    def solve_buttons(button_schematic, diagram):
        n_buttons = button_schematic.shape[0]
        min_presses = n_buttons + 1
        best_solution = None

        # Try all possible combinations of button presses (0 or 1)
        for x in product([0, 1], repeat=n_buttons):
            x_vec = np.array(x)
            # Check if the combination matches the diagram
            if np.array_equal((button_schematic.T @ x_vec) % 2, diagram):
                presses = np.sum(x_vec)
                if presses < min_presses:
                    min_presses = presses
                    best_solution = x_vec

        return best_solution, min_presses

    result = 0
    for diagram, button_schematic in zip(diagrams, button_schematics):
        res, num_presses = solve_buttons(np.array(button_schematic), diagram)
        result += num_presses

    return result


print(part1())


## Part 2
@timeit
def part2():
    # DOES NOT WORK
    # def solve_buttons(button_schematic, diagram):
    #     n_buttons = button_schematic.shape[0]
    #     min_presses = np.inf
    #     best_solution = None

    #     # Try all possible combinations of button presses (0 or 1)
    #     for x in product([0, 1], repeat=n_buttons):
    #         x_vec = np.array(x)
    #         # Check if the combination matches the diagram
    #         if np.array_equal((button_schematic.T @ x_vec), diagram):
    #             presses = np.sum(x_vec)
    #             if presses < min_presses:
    #                 min_presses = presses
    #                 best_solution = x_vec

    #     return best_solution, min_presses

    # def solve_buttons(button_schematic, diagram):
    #     n_buttons = button_schematic.shape[0]

    #     # Minimize total button presses
    #     c = np.ones(n_buttons)
    #     A_eq = button_schematic.T
    #     b_eq = diagram
    #     bounds = [(0, np.inf)] * n_buttons

    #     # Solve as a continuous problem first
    #     res = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method="simplex")

    #     if res.success:
    #         # Round to nearest integer and check if it matches
    #         x_sol = np.round(res.x).astype(int)
    #         if np.array_equal(A_eq @ x_sol, b_eq):
    #             return x_sol, np.sum(x_sol)

    #     return None, 0

    def solve_buttons(button_schematic, diagram, max_press=1000):
        n_buttons = button_schematic.shape[0]

        # Minimize total button presses
        c = np.ones(n_buttons)
        A_eq = button_schematic.T
        b_eq = diagram
        bounds = Bounds(0, max_press)
        integrality = np.full(n_buttons, 1)
        constraint = LinearConstraint(A_eq, b_eq, b_eq)

        res = milp(
            c=c,
            constraints=constraint,
            bounds=bounds,
            integrality=integrality,
            options={"disp": False},
        )

        if res.success:
            x_sol = np.round(res.x).astype(int)
            if np.array_equal(A_eq @ x_sol, b_eq):
                return x_sol, np.sum(x_sol)

        return None, 0

    result = 0
    for joltage, button_schematic in zip(joltages, button_schematics):
        res, num_presses = solve_buttons(np.array(button_schematic), joltage)
        print(num_presses)
        result += num_presses

    return result


print(part2())
