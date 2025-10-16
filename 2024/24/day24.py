## Pull Data
from collections import defaultdict
from pathlib import Path

from get_data import save_data, timeit

# save_data(2024, day := 24)
day=24
data = Path(f"2024/{day}/day{day:02d}.txt").read_text()
# data = Path(f"2024/{day}/day{day:02d}_sample.txt").read_text()

data_parts = data.split("\n\n")

wires = {}
for line in data_parts[0].splitlines():
    wire, value = line.split(": ")
    wires[wire] = value == "1"

gates = {}  # (input1, operation, input2) -> output

for line in data_parts[1].splitlines():
    wire1, operation, wire2, _, output = line.split(" ")
    gates[output] = (wire1, operation, wire2)

## Part 1
@timeit
def part1():
    unprocessed_wires = data_parts[1].splitlines()
    new_unprocessed_wires = []

    while unprocessed_wires:
        for line in unprocessed_wires:
            # Example: x00 AND y00 -> z00 becomes ['x00', 'AND', 'y00', '->', 'z00']
            wire1, operation, wire2, _, wire3 = line.split(" ")
            if wire1 not in wires or wire2 not in wires:
                new_unprocessed_wires.append(line)
                continue

            # AND gates output 1 if both inputs are 1; if either input is 0, these gates output 0.
            # OR gates output 1 if one or both inputs is 1; if both inputs are 0, these gates output 0.
            # XOR gates output 1 if the inputs are different; if the inputs are the same, these gates output 0.
            if operation == "AND":
                wires[wire3] = wires[wire1] and wires[wire2]
            elif operation == "OR":
                wires[wire3] = wires[wire1] or wires[wire2]
            elif operation == "XOR":
                wires[wire3] = wires[wire1] != wires[wire2]

        unprocessed_wires = new_unprocessed_wires
        new_unprocessed_wires = []

    # Gets all wires starting with "z", sort them alphabetically in reverse order
    result = ''.join('1' if wires[k] else '0' for k in sorted([k for k in wires if k.startswith('z')], reverse=True))

    return int(result, 2)


print(part1())


## Part 2
def part2():
    """Find swapped wires by checking adder structure patterns.
    
    sum[i] = x[i] XOR y[i] XOR carry[i-1]
    carry[i] = (x[i] AND y[i]) OR ((x[i] XOR y[i]) AND carry[i-1])
    """
    # Find highest z bit
    max_z = max(int(wire[1:]) for wire in gates if wire.startswith('z'))
    
    wrong = set()
    
    # Check each gate for violations
    for output, (in1, op, in2) in gates.items():
        
        # Rule 1: Output to a z wire must be XOR (except the final carry bit)
        # z-outputs (except last) must come from XOR - they're sum bits
        if output.startswith('z') and op != "XOR" and output != f"z{max_z:02d}":
            wrong.add(output)
        
        # Rule 2: XOR with inputs that aren't x or y wires must output to a z wire
        # These are the "sum = intermediate XOR carry" gates
        if op == "XOR":
            is_input_xor = (in1.startswith('x') or in1.startswith('y')) and \
                          (in2.startswith('x') or in2.startswith('y'))
            
            if not is_input_xor and not output.startswith('z'):
                wrong.add(output)
        
        # Rule 3: AND gates (except x00 AND y00) must feed into an OR gate
        # Part of carry propagation
        if op == "AND":
            is_first_bit = "x00" in (in1, in2) and "y00" in (in1, in2)
            
            if not is_first_bit:
                # Check if this output is used as input to an OR gate
                feeds_or = any(
                    gate_op == "OR" and output in (gate_in1, gate_in2)
                    for gate_out, (gate_in1, gate_op, gate_in2) in gates.items()
                )
                
                if not feeds_or:
                    wrong.add(output)
        
        # Rule 4: XOR gates with x or y inputs (except x00 and y00) must feed into another XOR
        # The intermediate XOR must combine with carry
        if op == "XOR":
            is_xy_inputs = (in1[0] in 'xy' and in2[0] in 'xy')
            is_first_bit = "x00" in (in1, in2) or "y00" in (in1, in2)
            
            if is_xy_inputs and not is_first_bit:
                # This should feed into another XOR gate
                feeds_xor = any(
                    gate_op == "XOR" and output in (gate_in1, gate_in2)
                    for gate_out, (gate_in1, gate_op, gate_in2) in gates.items()
                )
                
                if not feeds_xor:
                    wrong.add(output)
    
    return ','.join(sorted(wrong))

print(part2())