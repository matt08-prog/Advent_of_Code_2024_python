import math
import re
import numpy as np

lines = []
input_file_name = "test_input_1.txt"
# input_file_name = "test_input_2.txt"
# input_file_name = "test_input_3.txt"
# input_file_name = "test_input_4.txt"
# input_file_name = "test_input_5.txt"
# input_file_name = "real_input.txt"

trailheads = []
machines = []
debug = True


def print_i(string_to_print, debug_priorty=0):
    global debug
    if debug and debug_priorty > 1:
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
        x_target = int(re.findall(r"X=\d+", machine_str)[0][2:])
        x_target = int(re.findall(r"X=\d+", machine_str)[0][2:]) + 10000000000000
        # print(x_target)
        y_target = int(re.findall(r"Y=\d+", machine_str)[0][2:])
        y_target = int(re.findall(r"Y=\d+", machine_str)[0][2:]) + 10000000000000

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
    reverse = False
    if a_mult < 0:
        reverse = True

    # Check base case
    if high >= low:
 
        mid = (high + low) // 2
 
        # If element is present at the middle itself
        if target == mid * a_mult:
            return [mid]
 
        # If element is smaller than mid, then it can only
        # be present in left subarray
        elif not reverse and target < mid * a_mult or reverse and target > mid * a_mult:
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
    a_incs = machine.A_incs
    b_incs = machine.B_incs
    target = machine.target
    found = False
    searches = 0
    new_incs = [a_incs[0] - a_incs[1], b_incs[0] - b_incs[1]]
    new_target = target[0] - target[1]
    # print_i(type(target))
    # print_i(type(result))

    low_b = 0
    mid_b = 0 # num B presses
    # high_b = 10000000000000
    high_b = 100
    
    low_a = 0 # might need to round instead of int()
    # mid_a = 5000000000000 # num A presses
    mid_a = 0 # might need to round instead of int()
    high_a = 100 # might need to round instead of int()
    # high_a = 100

    passed = 0

    if new_incs[1] == 0:
        mid_a = int(new_target / new_incs[0])
        print_i(f"special case; a_presses: {mid_a}", 1)
        a_contribution = a_incs[0] * mid_a
        b_contribution = b_incs[1] * mid_b
        correct_num_b_presses = binary_search_find_multiple_of_value(target[0] - a_contribution, low_b, high_b, b_incs[0])
        print_i(f"\tspecial case; looking for {b_incs[0]} * B to equal {new_target - a_contribution}", 1)
        print_i(f"special case; b_pressed: {correct_num_b_presses}", 1)
        result = (mid_a * a_incs) + (correct_num_b_presses * b_incs)
        print_i(f"result should equal target; {result} == {target}\n\n", 1)
        if np.array_equal(result, target):
            found = True
            print_i(f"\tfound answer: {mid_a} A presses and {mid_b} B presses", 2)
            mid_b = correct_num_b_presses[0]
            final_answer += 3 * mid_a + mid_b
            solved_machines.append([a_incs, b_incs, target])
            solvable_machines += 1
            continue
    
    result = (mid_a * new_incs[0]) + (mid_b * new_incs[1])

    first = True
    truthy_was = True

    # print(low_a)
    # print(high_a)

    print_i(f"incs: X={new_incs[0]}, Y={new_incs[1]}", 1)
    print_i(f"Prize: X={target[0]}, Y={target[1]}", 1)

    gcd_1 = math.gcd(a_incs[0], b_incs[0])
    gcd_2 = math.gcd(a_incs[1], b_incs[1])

    if divmod(target[0], gcd_1)[1] != 0 or divmod(target[1], gcd_2)[1] != 0:
        print_i("\tnot found", 1)
        continue

    while found == False:
        # if not result == new_target:
        searches += 1
        if searches > 10000:
            print_i(f" gave up")
            break
        print_i(f"result: {result} != target: {new_target}       a's: {mid_a}, b's: {mid_b}", 1)
        a_contribution = new_incs[0] * mid_a
        b_contribution = new_incs[1] * mid_b

        print_i(f"\tlooking for {new_incs[1]} * B to equal {new_target - a_contribution}", 1)
        # Testing for X value
        correct_num_b_presses = binary_search_find_multiple_of_value(new_target - a_contribution, low_b, high_b, new_incs[1])
        if len(correct_num_b_presses) == 1:
            print_i(f"correct_num_b_presses= {correct_num_b_presses}", 1)
            mid_b = correct_num_b_presses[0]
            b_contribution = new_incs[1] * mid_b
            if a_contribution + b_contribution == new_target:
                result = (mid_a * a_incs) + (mid_b * b_incs)
                if np.array_equal(result, target):
                    found = True
                    break
        correct_num_b_presses = 0
        # if len(correct_num_b_presses) == 1:
        #     # found presses that work for X, now see if it works for Y
        #     print_i(f"\t\tfound presses that work for X, now seeing if it works for Y")
        #     a_y_contribution = new_incs[1] * mid_a
        #     b_y_contribution = new_incs[1] * correct_num_b_presses[0]

        #     # Testing for Y value
        #     # correct_num_b_presses = binary_search_find_multiple_of_value(target[1] - a_y_contribution, low_b, high_b, mid_b, b_incs[1])
        #     # if correct_num_b_presses != -1:
        #     if a_y_contribution + b_y_contribution == new_target:
        #         mid_b = correct_num_b_presses[0]
        #         found = True
        #         break
        
        
        
        result = (mid_a * new_incs[0]) + (mid_b * new_incs[1])
        mid_a += 1
        # else:
        #     print_i(f"\tfound answer: {mid_a} A presses and {mid_b} B presses\t {result} == {new_target}", 1)
            # result = (mid_a * a_incs) + (mid_b * b_incs)

        # break

    if found:
        print_i(f"\tfound answer: {mid_a} A presses and {mid_b} B presses", 2)
        final_answer += 3 * mid_a + mid_b
        solved_machines.append([a_incs, b_incs, target])
        solvable_machines += 1
    else:
        print_i("\tnot found", 1)

# print(f"\n\n {solved_machines}")
print(f"solvable machines: {solvable_machines}") # final answer: 29436
print(final_answer) # final answer: 29436