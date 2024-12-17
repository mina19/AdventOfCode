## Pull Data
import re
from pathlib import Path

from get_data import save_data, timeit

save_data(2024, day := 17)
data = Path(f"2024/{day}/day{day:02d}.txt").read_text()
# data = Path(f"2024/{day}/day{day:02d}_sample.txt").read_text()

register_pattern = "Register (.): (\d+)"

registers_original = {}
for line in data.split("\n\n")[0].split("\n"):
    match = re.match(register_pattern, line)
    registers_original[match[1]] = int(match[2])

instructions = [
    int(num)
    for num in data.split("\n\n")[1].splitlines()[0].split("Program: ")[1].split(",")
]


## Part 1
@timeit
def part1(registers):
    i = 0
    outputs = []
    registers = registers.copy()
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
            combo_operand = registers[combo_dict[operand]]

        if opcode == 0:
            # The adv instruction (opcode 0) performs division.
            # The numerator is the value in the A register.
            # The denominator is found by raising 2 to the power of the
            # instruction's combo operand.
            registers["A"] = registers["A"] // 2**combo_operand
        elif opcode == 1:
            # The bxl instruction (opcode 1) calculates the bitwise XOR
            # of register B and the instruction's literal operand,
            # then stores the result in register B.
            registers["B"] = registers["B"] ^ operand
        elif opcode == 2:
            # The bst instruction (opcode 2) calculates the value of its
            # combo operand modulo 8 (thereby keeping only its lowest 3 bits),
            # then writes that value to the B register.
            registers["B"] = combo_operand % 8
        elif opcode == 3:
            # The jnz instruction (opcode 3) does nothing if the A register
            # is 0. However, if the A register is not zero, it jumps by
            # setting the instruction pointer to the value of its literal operand;
            # if this instruction jumps, the instruction pointer is not increased
            # by 2 after this instruction.
            if registers["A"] != 0:
                i = operand
        elif opcode == 4:
            # The bxc instruction (opcode 4) calculates the bitwise XOR of
            # register B and register C, then stores the result in register B.
            # (For legacy reasons, this instruction reads an operand but ignores it.)
            registers["B"] = registers["B"] ^ registers["C"]
        elif opcode == 5:
            # The out instruction (opcode 5) calculates the value of its
            # combo operand modulo 8, then outputs that value.
            # (If a program outputs multiple values, they are separated by commas.)
            outputs.append(combo_operand % 8)
        elif opcode == 6:
            # The bdv instruction (opcode 6) works exactly like the adv
            # instruction except that the result is stored in the B register.
            # (The numerator is still read from the A register.)
            registers["B"] = registers["A"] // 2**combo_operand
        elif opcode == 7:
            # The cdv instruction (opcode 7) works exactly like the adv instruction
            # except that the result is stored in the C register.
            # (The numerator is still read from the A register.)
            registers["C"] = registers["A"] // 2**combo_operand

    # Join the values it output into a single string
    return ",".join(str(x) for x in outputs)


print(part1(registers_original))


## Part 2
# This is a brute force approach and will take a long time to run for large inputs
@timeit
def part2():
    desired_output = data.split("\n\n")[1].splitlines()[0].split("Program: ")[1]
    register_a_value = 1
    while True:
        registers = registers_original.copy()
        registers["A"] = register_a_value
        program_output = part1(registers)
        if program_output == desired_output:
            break
        register_a_value += 1
    return register_a_value


print(part2())
