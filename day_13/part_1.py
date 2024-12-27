import re
import numpy as np

lines = []
input_file_name = "test_input_1.txt"
input_file_name = "test_input_2.txt"
input_file_name = "test_input_3.txt"
# input_file_name = "test_input_4.txt"
# input_file_name = "test_input_5.txt"
# input_file_name = "real_input.txt"

trailheads = []
machines = []
debug = True


def print_i(string_to_print, debug_priorty=0):
    global debug
    if debug and debug_priorty > 0:
        print(string_to_print)

class DotDict(dict):
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as k:
            raise AttributeError(k)

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError as k:
            raise AttributeError(k)

with open(input_file_name) as file:
    col_index = 0
    for line in file:
        lines.append(line.strip())
    for machine_index in range(0, len(lines), 4):
        machine_str = "".join(lines[machine_index:machine_index+3])
        # print(machine_str)
        X_incs = [int(i[2:]) for i in re.findall(r"X\+\d+", machine_str)]
        # print(X_incs)
        Y_incs = [int(i[2:]) for i in re.findall(r"Y\+\d+", machine_str)]
        # print(Y_incs)
        # x_target = [int(i[2:]) for i in re.findall(r"X=\d+", machine_str)]
        x_target = int(re.findall(r"X=\d+", machine_str)[0][2:])
        # print(x_target)
        # y_target = [int(i[2:]) for i in re.findall(r"Y=\d+", machine_str)]
        y_target = int(re.findall(r"Y=\d+", machine_str)[0][2:])
        # print(y_target)
        # machine = DotDict({"A_incs": [X_incs[0], Y_incs[0]], "B_incs": [X_incs[1], Y_incs[1]], "target": [x_target, y_target]})
        machine = DotDict({"A_incs": np.array([X_incs[0], Y_incs[0]]), "B_incs": np.array([X_incs[1], Y_incs[1]]), "target": np.array([x_target, y_target])})
        
        # print(machine.A_incs)
        machines.append(machine)

print(lines)

# print()

# print(trailheads)
final_answer = 0

def binary_search_find_multiple_of_value(target, low, high, a_mult):
 
    mid = (high + low) // 2

    # Check base case
    if high >= low:
 
        mid = (high + low) // 2
 
        # If element is present at the middle itself
        if target == mid * a_mult:
            return [mid]
 
        # If element is smaller than mid, then it can only
        # be present in left subarray
        elif target < mid * a_mult:
            # print_i(f"{target}")
            return binary_search_find_multiple_of_value(target, low, mid - 1, a_mult)
 
        # Else the element can only be present in right subarray
        else:
            return binary_search_find_multiple_of_value(target, mid + 1, high, a_mult)

    else:
        # Element is not present in the array
        return [-1, mid]

solvable_machines = 0
solved_machines = []

for machine in machines:

    low_a = 0
    mid_a = 0 # num A presses
    high_a = 100

    low_b = 0
    mid_b = 0 # num B presses
    high_b = 100

    a_incs = machine.A_incs
    b_incs = machine.B_incs
    target = machine.target
    result = (mid_a * a_incs) + (mid_b * b_incs)
    found = False
    searches = 0
    # print_i(type(target))
    # print_i(type(result))

    print_i(f"Prize: X={target[0]}, Y={target[0]}", 1)

    while True:
        if not np.array_equal(result, target):
            searches += 1
            if searches > 100:
                print_i(f" gave up")
                break
            print_i(f"result: {result} != target: {target}       a's: {mid_a}, b's: {mid_b}")
            a_x_contribution = a_incs[0] * mid_a
            b_x_contribution = b_incs[0] * mid_b

            print_i(f"\tlooking for {b_incs[0]} * x to equal {target[0] - a_x_contribution}")
            # Testing for X value
            correct_num_b_presses = binary_search_find_multiple_of_value(target[0] - a_x_contribution, low_b, high_b, b_incs[0])

            if len(correct_num_b_presses) == 1:
                # found presses that work for X, now see if it works for Y
                print_i(f"\t\tfound presses that work for X, now seeing if it works for Y")
                a_y_contribution = a_incs[1] * mid_a
                b_y_contribution = b_incs[1] * correct_num_b_presses[0]

                # Testing for Y value
                # correct_num_b_presses = binary_search_find_multiple_of_value(target[1] - a_y_contribution, low_b, high_b, mid_b, b_incs[1])
                # if correct_num_b_presses != -1:
                if a_y_contribution + b_y_contribution == target[1]:
                    mid_b = correct_num_b_presses[0]
                    found = True
                    break
            
            mid_a += 1
            # mid_b = correct_num_b_presses[1]

            # # A presses wasn't right, need to update its value
            # if a_x_contribution + b_x_contribution < target[0]:
            #     # must be in right hand side
            #     low_a = mid_a + 1
            #     high_a = high_a
            #     mid_a = (high_a + low_a) // 2
            # else:
            #     # must be in left hand side
            #     low_a = low_a
            #     high_a = mid_a - 1
            #     mid_a = (high_a + low_a) // 2
            
            result = (mid_a * a_incs) + (mid_b * b_incs)

        # break

    if found:
        print_i(f"\tfound answer: {mid_a} A presses and {mid_b} B presses", 1)
        final_answer += 3 * mid_a + mid_b
        solved_machines.append([a_incs, b_incs, target])
        solvable_machines += 1
    else:
        print_i("\tnot found", 1)


    # print_i(f"A -> X: {machine}")

print(f"\n\n {solved_machines}")
print(f"solvable machines: {solvable_machines}") # final answer: 29436
print(final_answer) # final answer: 29436