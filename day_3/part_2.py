import re
lines = []
# input_file_name = "test_input_1.txt"
input_file_name = "test_input_2.txt"
# input_file_name = "real_input.txt"

with open(input_file_name) as file:
    for line in file:
        lines.append(line)
print(lines)

mul_results_sum = 0
multiply_instructions = []
multiply_instruction_locations = []
should_do = False

for line in lines:
    multiply_instruction_matches = re.finditer(r"mul\([0-9]+,[0-9]+\)", line)

    for match in multiply_instruction_matches:
        multiply_instructions.append(match.group())
        multiply_instruction_locations.append(match.start())

    print(multiply_instructions)
    print(multiply_instruction_locations)
    dos = re.finditer(r"do\(\)", line)

    dos_locations = [0]
    dos_locations.append(*[i.start() for i in dos])
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
    print(f"dos: {dos_locations}")
    # if len(dont_locations) == 0:
    #     should_do = True
    should_break = False

    for instruction in multiply_instructions:
        while True:
            if multiply_instruction_locations[0] > next_start:
                # past a do
                # if multiply_instruction_locations[0] > next_stop and not should_do:
                if multiply_instruction_locations[0] > next_stop:
                    # past a don't
                    print(f"stopped because {multiply_instruction_locations[0]} > {next_stop}")
                    multiply_instruction_locations.pop(0)
                    if len(dos_locations) != 0:
                        next_start = dos_locations.pop(0)
                        print(f"\tstopping until {next_start}")
                    if len(multiply_instruction_locations) == 0:
                        should_break = True
                        break
                    break
                else:
                    # not past a don't 
                # else:
                #     if len(dont_locations) == 0:
                #         should_do = True
                #     else:
                #         next_stop = dont_locations.pop(0)
                    if len(dont_locations) != 0:
                        next_stop = dont_locations.pop(0)
                        # should_do = True

                    nums = [int(i) for i in re.findall(r"[0-9]+", instruction)]
                    product = nums[0] * nums[1]
                    mul_results_sum += product
                    # print(nums)
                    # print(product)
                    print(f"location {multiply_instruction_locations[0]}: {product} = {nums[0]} * {nums[1]}\t next_stop {next_stop}\t should_do {should_do}")
                    multiply_instruction_locations.pop(0)
                    if len(multiply_instruction_locations) == 0:
                        should_break = True
                        break
                    break
            else:
                if len(multiply_instruction_locations) == 0:
                    should_break = True
                    break
                else:
                    multiply_instruction_locations.pop(0)

        if should_break:
            break

        # if not should_do:
        #     next_stop = dont_locations[0]
        # next_start = dos_locations[0]

        # if multiply_instruction_locations[0] < next_stop:
        #     multiply_instruction_locations.pop(0)
        #     if multiply_instruction_locations[0] > next_start:
        #         dont_locations.pop(0)
        #     if len(multiply_instruction_locations) == 0:
        #         break
        # else:



print(f"final result: {mul_results_sum}") # answer: 160672468