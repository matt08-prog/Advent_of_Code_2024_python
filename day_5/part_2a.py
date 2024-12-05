import re
lines = []
# input_file_name = "test_input_1.txt"
# input_file_name = "test_input_2.txt"
# input_file_name = "test_input_3.txt"
input_file_name = "real_input.txt"

with open(input_file_name) as file:
    for line in file:
        lines.append(line)
print(len(lines))

mul_results_sum = 0
do_period = True

for line in lines:
    multiply_instructions = []
    multiply_instruction_locations = []
    multiply_instruction_matches = re.finditer(r"mul\([0-9]+,[0-9]+\)", line)

    for match in multiply_instruction_matches:
        multiply_instructions.append(match.group())
        multiply_instruction_locations.append(match.start())

    print(multiply_instructions)
    print(multiply_instruction_locations)
    dos = re.finditer(r"do\(\)", line)

    # dos_locations = [0]
    dos_locations = []
    start_locations = [i.start() for i in dos]
    for locations in start_locations:
        # dos_locations.append(*[i.start() for i in dos])
        dos_locations.append(locations)
    print(f"dos: {dos_locations}")

    donts = re.finditer(r"don't\(\)", line)

    dont_locations = [i.start() for i in donts]
    print(f"don'ts {dont_locations}")

    # donts = re.finditer(r"don\'t\(\)", line)
    # print(multiply_instructions)
    next_stop = dont_locations[0]
    next_start = dos_locations[0]
    dos_locations.pop(0)
    dont_locations.pop(0)
    print(f"dos: {dos_locations}\n")
    # if len(dont_locations) == 0:
    #     should_do = True
    should_break = False

    # for instruction in multiply_instructions:

    while True:
        assert(len(multiply_instruction_locations) == len(multiply_instructions))
        if len(multiply_instruction_locations) == 0:
            # should_break = True
            print(f"next_stop: {next_stop}")
            if next_stop != instruction_location + 1:
                do_period = False
            break
        instruction = multiply_instructions[0]
        instruction_location = multiply_instruction_locations[0]
        if do_period:
            if instruction_location < next_stop:
                nums = [int(i) for i in re.findall(r"[0-9]+", instruction)]
                product = nums[0] * nums[1]
                mul_results_sum += product
                print(f"{instruction_location}: in a do period ({instruction_location} < {next_stop}) {multiply_instruction_locations[0]}: {product} = {nums[0]} * {nums[1]}\t next_stop {next_stop}\t do_period {do_period}")
                if len(multiply_instruction_locations) == 0:
                    # should_break = True
                    
                    break
                multiply_instruction_locations.pop(0)
                multiply_instructions.pop(0)
                continue
            else:
                print(f"{instruction_location}: no longer a do_period ({instruction_location} > {next_stop})")
                do_period = False
                # if len(dont_locations) != 0:
                #     next_stop = dont_locations.pop(0)
                while instruction_location > next_start:
                    if len(dos_locations) != 0:
                        next_start = dos_locations.pop(0)
                    else:
                        next_start = multiply_instruction_locations[-1] + 1

                if len(multiply_instruction_locations) == 0:
                    # should_break = True
                    break
                multiply_instruction_locations.pop(0)
                multiply_instructions.pop(0)
        elif not do_period:
            if instruction_location > next_start:
                print(f"{instruction_location}: now a do_period again ({instruction_location} > {next_start})")
                if instruction_location > next_start:
                    do_period = True
                    while instruction_location > next_stop:
                        if len(dont_locations) != 0:
                            next_stop = dont_locations.pop(0)
                        else:
                            next_stop = multiply_instruction_locations[-1] + 1

                    # if len(dos_locations) != 0:
                    #     next_start = dos_locations.pop(0)
            else:
                if len(multiply_instruction_locations) == 0:
                    # should_break = True
                    break
                multiply_instruction_locations.pop(0)
                multiply_instructions.pop(0)
        # if should_break:
        #     break

print(f"final result: {mul_results_sum}") 
# answer: 75,078,675 is too low
# answer: 107,565,988 is too high
# answer: 116,837,282 is too high
# answer: 93,733,733 is wrong
# answer: 93,289,293 is wrong

# answer: 84893551 is correct