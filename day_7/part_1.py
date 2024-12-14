import re
# input_file_name = "test_input_1.txt"
input_file_name = "real_input.txt"
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
            print(equation_obj)

    # for line in lines[start_of_updates:]:
    #     stripped_line = line.strip().split(",")
    #     int_array = [int(i) for i in stripped_line]
    #     updates.append(int_array)

print(f"updates: {updates}")

final_answer = 0
operators = 0 # 0 = +; 1 = *

for equation_index, equation in enumerate(equations):
    print(equation_index)
    num_operands = len(equation["operands"])
    for index in range(2**(num_operands-1)):
        total = int(equation["operands"][0])
        bin_index = bin(index)
        for i in range(0, num_operands-1):
            operator = (index >> i) & 1
            if operator == 0:
                total += int(equation["operands"][i+1])
            elif operator == 1:
                total *= int(equation["operands"][i+1])
            # print(f"equation: {equation}, i: {i}, index: {index}, , opeator = {operator}, gave total: {total}")
        if total == equation["answer"]:
            final_answer += total
            break



print(f"final_answer: {final_answer}") # answer: 3119088655389