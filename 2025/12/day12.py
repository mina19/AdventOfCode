## Pull Data
from pathlib import Path

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp

# from get_data import save_data, timeit

# save_data(year := 2025, day := 1)
day = 12
year = 2025
data = Path(f"{year}/{day}/day{day:02d}.txt").read_text()
# data = Path(f"{year}/{day}/day{day:02d}_sample.txt").read_text()

# Put in additional \n manually in txt files for easier parsing
present_shapes_data = data.split('\n\n\n')[0]
requirements_data = data.split('\n\n\n')[1]

present_shapes = {}

present_blocks = present_shapes_data.strip().split('\n\n')

for block in present_blocks:
    lines = block.strip().split('\n')
    present_id = int(lines[0].rstrip(':'))
    grid_rows = lines[1:]
    
    grid = []
    for row in grid_rows:
        grid.append([1 if char == '#' else 0 for char in row])
    
    present_shapes[present_id] = np.array(grid)

requirements = []
    
for line in requirements_data.strip().split('\n'):
    grid_part, counts_part = line.split(': ')
    
    width, height = map(int, grid_part.split('x'))
    grid_size = (width, height)
    
    present_counts = {
        present_id: count 
        for present_id, count in enumerate(map(int, counts_part.split()))
    }
    
    requirements.append({
        'grid_size': grid_size,
        'present_counts': present_counts
    })

def get_all_orientations(shape):
    orientations = set()
    current = shape
    
    for _ in range(4):  # 4 rotations
        # Add original and flipped
        orientations.add(tuple(map(tuple, current)))
        orientations.add(tuple(map(tuple, np.flip(current, axis=1))))
        # Rotate 90 degrees
        current = np.rot90(current)
    
    return [np.array(o) for o in orientations]

def get_all_placements(present_id, grid_size):
    width, height = grid_size
    shape = present_shapes[present_id]
    placements = []
    
    # Get all unique orientations
    orientations = get_all_orientations(shape)
    
    for orientation in orientations:
        shape_h, shape_w = orientation.shape
        
        # Try all positions where it fits in bounds
        for row in range(height - shape_h + 1):
            for col in range(width - shape_w + 1):
                placements.append((row, col, orientation))
    
    return placements

# Works for sample input but does not work for real problem...........
def can_fit_milp(req):
    grid_size = req['grid_size']
    present_counts = req['present_counts']
    width, height = grid_size
    
    # Generate all possible placements for each present
    all_placements = []
    present_to_placements = {}
    
    for present_id, count in present_counts.items():
        if count > 0:
            start_idx = len(all_placements)
            placements = get_all_placements(present_id, grid_size)
            all_placements.extend(placements)
            end_idx = len(all_placements)
            present_to_placements[present_id] = list(range(start_idx, end_idx))
    
    num_placements = len(all_placements)
    
    if num_placements == 0:
        return True  # No presents needed
    
    # Decision variables: x[i] = 1 if placement i is selected
    c = np.zeros(num_placements)  # Objective is feasibility only
    
    # Build constraint matrix
    # Constraint 1: Each cell covered at most once
    # For each cell (i, j), sum of all placements covering it ≤ 1
    A_cell = []
    b_cell_upper = []
    
    for cell_row in range(height):
        for cell_col in range(width):
            constraint_row = np.zeros(num_placements)
            
            # Check which placements cover this cell
            for p_idx, (row, col, orientation) in enumerate(all_placements):
                shape_h, shape_w = orientation.shape
                
                # Does this placement cover cell (cell_row, cell_col)?
                if row <= cell_row < row + shape_h and col <= cell_col < col + shape_w:
                    local_row = cell_row - row
                    local_col = cell_col - col
                    if orientation[local_row, local_col] == 1:
                        constraint_row[p_idx] = 1
            
            A_cell.append(constraint_row)
            b_cell_upper.append(1)  # At most 1 present covers this cell
    
    A_cell = np.array(A_cell)
    b_cell_lower = np.zeros(len(b_cell_upper))  # At least 0 (no lower bound really)
    
    # Constraint 2: Each present used exactly required number of times
    A_present = []
    b_present = []
    
    for present_id, count in present_counts.items():
        if count > 0:
            constraint_row = np.zeros(num_placements)
            
            # Mark all placements of this present
            for p_idx in present_to_placements[present_id]:
                constraint_row[p_idx] = 1
            
            A_present.append(constraint_row)
            b_present.append(count)  # Exactly 'count' of this present
    
    A_present = np.array(A_present)
    b_present = np.array(b_present)
    
    # Combine constraints
    A = np.vstack([A_cell, A_present, -A_present])  # -A for equality (>= and <=)
    b_lower = np.concatenate([b_cell_lower, b_present, -b_present])
    b_upper = np.concatenate([b_cell_upper, b_present, -b_present])
    
    constraints = LinearConstraint(A, b_lower, b_upper)
    
    # Binary variables
    integrality = np.ones(num_placements)  # 1 = integer variable
    bounds = Bounds(lb=0, ub=1)  # Binary: 0 or 1
    
    # Solve
    result = milp(
        c=c,
        constraints=constraints,
        integrality=integrality,
        bounds=bounds
    )
    
    return result.success


def part1_does_not_scale():
    feasible_count = 0
    
    for i, req in enumerate(requirements):
        if can_fit_milp(req):
            feasible_count += 1
    
    return feasible_count




def part1_imgoingtobemadifthisworks():
    # Check the obvious
    # Calculate areas for each present
    present_areas = np.array([
        np.sum(present_shapes[i]) if i in present_shapes else 0
        for i in range(len(present_shapes))
    ])
    
    feasible_count = 0
    for i, req in enumerate(requirements):
        width, height = req['grid_size']
        grid_area = width * height
        
        # Calculate total area needed for this requirement
        present_counts_array = np.array([
            req['present_counts'][j] 
            for j in range(len(present_shapes))
        ])
        
        total_present_area = np.sum(present_areas * present_counts_array)
        
        if grid_area >= total_present_area:
            feasible_count += 1
    
    return feasible_count

# This is not a general solution.....
print(part1_imgoingtobemadifthisworks())


## Part 2
# @timeit
def part2():
    pass


part2()
