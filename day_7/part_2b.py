import re
import sys
input_file_name = "test_input_1.txt"
# input_file_name = "test_input_2.txt"
# input_file_name = "test_input_3.txt"
# input_file_name = "test_input_4.txt"
# input_file_name = "test_input_5.txt"
input_file_name = "real_input.txt"
equations = []
start_of_updates = 0
updates = []
debug = True
debug = False

with open(input_file_name) as file:
    lines = file.readlines()
    
    for line in lines:
        # lines.append(line.strip())
        if line != "\n":
            # print(line[0:2])
            numbers_from_line = re.findall("\d+", line)
            equation_obj = {"answer":int(numbers_from_line[0]), "operands": numbers_from_line[1:]}
            equations.append(equation_obj)
            # print(equation_obj)

final_answer = 0
operators = 0 # 0 = +; 1 = *; 2 = ||
exited = False
# print(sys.maxsize)
for equation_index, equation in enumerate(equations):
    print(equation_index)
    if debug:
        print(f"equation: {equation}")
    num_operands = len(equation["operands"])
    # skipped = 0
    index = 0
    # final_goal = 3**(num_operands-1)
    target_answer = equation["answer"]
    num_2s = 0
    num_3s = 0
    # while index < final_goal:
    while True:
        total = int(equation["operands"][0])
        if num_2s < num_operands-1:
            num_2s = 0
            num_3s = 0

            for i in range(0, num_operands-1):
            # for i in range(num_operands-2, 0, -1):
                operator = (index >> i*2) & 3
                if operator == 3:
                    num_3s = 1
                    break
            
            if num_3s == 0:

                for i in range(0, num_operands-1):
                # for i in range(num_operands-2, 0, -1):
                    operator = (index >> i*2) & 3
                    if operator == 3:
                        num_3s = 1
                        
                    # if operator == 3:
                    #     # index += 1
                    #     # skipped += 1
                    #     final_goal += 1
                    #     exited = True
                    #     break
                    if operator == 0:
                        total += int(equation["operands"][i+1])
                    elif operator == 1:
                        total *= int(equation["operands"][i+1])
                    elif operator == 2:
                        num_2s += 1
                        total = int(str(total) + equation["operands"][i+1])
                    width = (num_operands - 1) * 2
                    binary_string = f'{index:0{width}b}'
                    if debug:
                        print(f"\t\tsearching: {binary_string}: {index}")

                width = (num_operands - 1) * 2
                binary_string = f'{index:0{width}b}'
                if debug:
                    print(f"searching: {binary_string}: {index}")
            # print(equation["operands"])
            # print(f"\tindex: {index}, i: {i}, opeator = {operator}, gave total: {total}, num_twos: {num_2s}, num_operands: {num_operands}")
        elif num_2s == num_operands - 1:
            width = (num_operands - 1) * 2
            binary_string = f'{index:0{width}b}'
            if debug:
                print(f"not found: {binary_string}: {index}")
            if binary_string != ("10" * (num_operands - 2)) + "11":
                print("error 1")
                exit(-1)
            break
        else:
            print("error 2")
            exit(-1)
        if total == target_answer and exited == False:
            final_answer += total
            if debug:
                # print(f"{index:9b}")
                # print(f"{index}")
                width = (num_operands - 1) * 2
                binary_string = f'{index:0{width}b}'
                if debug:
                    print(binary_string)
                for operand_index, operand in enumerate(equation["operands"]):
                    sign = ""
                    match (index >> operand_index*2) & 3:
                        case 0:
                            sign = " + "
                        case 1:
                            sign = " * "
                        case 2:
                            sign = " || "
                        case _:
                            sign = "ERROR"
                    
                    binary_string = f'{operand} {sign}'
                    print(binary_string, end="")
            # print(format(index, "05b"))
                print()
            break
        index += 1
        exited = False
    # print(f"skipped: {skipped}")

# 527917185924 is too low
# 264184044732519 is too high
# 264183924871929 is too low
# 264184745723230 is wrong
print(f"final_answer: {final_answer}") # answer: 264184041398847
