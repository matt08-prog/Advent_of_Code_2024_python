import re
import sys
# input_file_name = "test_input_1.txt"
# input_file_name = "test_input_2.txt"
input_file_name = "test_input_3.txt"
# input_file_name = "real_input.txt"
equations = []
start_of_updates = 0
updates = []

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
    num_operands = len(equation["operands"])
    print(f"equation: {equation}")
    skipped = 0
    index = 0
    final_goal = 3**(num_operands-1)
    target_answer = equation["answer"]
    while index < final_goal:
    # for index in range(3**(num_operands-1)):
        # print("---------------------------------------")
        total = int(equation["operands"][0])
        # if index % 3 == 0 and index > 0:
        #     continue
        for i in range(0, num_operands-1):
            operator = (index >> i*2) & 3
            if operator == 3:
                # index += 1
                # skipped += 1
                final_goal += 1
                exited = True
                break
            elif operator == 0:
                total += int(equation["operands"][i+1])
            elif operator == 1:
                total *= int(equation["operands"][i+1])
            elif operator == 2:
                # old_total = total
                total = int(str(total) + equation["operands"][i+1])
                # if len(str(total)) > 16:
                #     exit(-1)
            if total > target_answer:
                break

            print(f"\tindex: {index}, i: {i}, opeator = {operator}, gave total: {total}")
        index += 1
        if total == target_answer and exited == False:
            final_answer += total
            break
        exited = False
    # print(f"skipped: {skipped}")

print(f"final_answer: {final_answer}") # answer: 
# 527917185924 is too low
# 264184044732519 is too high
# 264183924871929 is too low