## Pull Data
import re
from pathlib import Path
from z3 import BitVec, BitVecVal, Optimize, LShR

from get_data import save_data, timeit

save_data(2024, day := 17)
data = Path(f"2024/{day}/day{day:02d}.txt").read_text()
# data = Path(f"2024/{day}/day{day:02d}_sample.txt").read_text()

register_pattern = r"Register (.): (\d+)"

register = {}
for line in data.split("\n\n")[0].split("\n"):
    match = re.match(register_pattern, line)
    register[match[1]] = int(match[2])

instructions = [
    int(num)
    for num in data.split("\n\n")[1].splitlines()[0].split("Program: ")[1].split(",")
]


## Part 1
@timeit
def part1():
    i = 0
    outputs = []
    while i < len(instructions) - 1:
        # Get the literal opcode and operand
        opcode = instructions[i]
        i += 1
        operand = instructions[i]
        i += 1

        combo_operand = operand
        # Combo operands 0 through 3 represent literal values 0 through 3.
        # Combo operand 4 represents the value of register A.
        # Combo operand 5 represents the value of register B.
        # Combo operand 6 represents the value of register C.
        # Combo operand 7 is reserved and will not appear in valid programs.
        combo_dict = {
            4: "A",
            5: "B",
            6: "C",
        }
        if 3 < operand < 7:
            combo_operand = register[combo_dict[operand]]

        if opcode == 0:
            # The adv instruction (opcode 0) performs division.
            # The numerator is the value in the A register.
            # The denominator is found by raising 2 to the power of the
            # instruction's combo operand.
            register["A"] = register["A"] // (1 << combo_operand)
        elif opcode == 1:
            # The bxl instruction (opcode 1) calculates the bitwise XOR
            # of register B and the instruction's literal operand,
            # then stores the result in register B.
            register["B"] = register["B"] ^ operand
        elif opcode == 2:
            # The bst instruction (opcode 2) calculates the value of its
            # combo operand modulo 8 (thereby keeping only its lowest 3 bits),
            # then writes that value to the B register.
            register["B"] = combo_operand % 8
        elif opcode == 3:
            # The jnz instruction (opcode 3) does nothing if the A register
            # is 0. However, if the A register is not zero, it jumps by
            # setting the instruction pointer to the value of its literal operand;
            # if this instruction jumps, the instruction pointer is not increased
            # by 2 after this instruction.
            if register["A"] != 0:
                i = operand
        elif opcode == 4:
            # The bxc instruction (opcode 4) calculates the bitwise XOR of
            # register B and register C, then stores the result in register B.
            # (For legacy reasons, this instruction reads an operand but ignores it.)
            register["B"] = register["B"] ^ register["C"]
        elif opcode == 5:
            # The out instruction (opcode 5) calculates the value of its
            # combo operand modulo 8, then outputs that value.
            # (If a program outputs multiple values, they are separated by commas.)
            outputs.append(combo_operand % 8)
        elif opcode == 6:
            # The bdv instruction (opcode 6) works exactly like the adv
            # instruction except that the result is stored in the B register.
            # (The numerator is still read from the A register.)
            register["B"] = register["A"] // (1 << combo_operand)
        elif opcode == 7:
            # The cdv instruction (opcode 7) works exactly like the adv instruction
            # except that the result is stored in the C register.
            # (The numerator is still read from the A register.)
            register["C"] = register["A"] // (1 << combo_operand)

    # Join the values it output into a single string
    return ",".join(str(x) for x in outputs)


print(part1())


## Part 2
# This ONLY works for my input. For someone else's input they need
# to figure out the order in which their instructions are called
# and modify the iterated steps for how a, b, c change.
@timeit
def part2():
    # Initialize bit vectors
    A = BitVec("A", 64)
    b = BitVecVal(0, 64)
    c = BitVecVal(0, 64)

    # Setup solver
    solver = Optimize()
    a = A  # This is necessary - can't modify A directly

    # Process each instruction
    for i in range(len(instructions)):
        # Sequence of bit operations
        b = a % 8  # opcode 2, operand 4 (get lowest 3 bits)
        b = b ^ 1  # opcode 1, operand 1 (XOR with 1)
        c = LShR(
            a, b
        )  # c = a // (1 << b) # opcode 7, operand 5 (logical shift right by b)
        b = b ^ c  # opcode 4, operand 7 (XOR with shifted value)
        b = b ^ 4  # opcode 1, operand 4 (XOR with 4)
        a = LShR(
            a, 3
        )  # a = a // (1 << 3) # opcode 0, operand 3 (logical shift right by 3)
        solver.add(b % 8 == instructions[i])  # opcode 5, operand 5 (the output)

    # Find minimum value of A that satisfies constraints
    solver.minimize(A)

    # Return result if found
    if solver.check().r == 1:
        model = solver.model()
        return model[A].as_long()
    return None


print(part2())
