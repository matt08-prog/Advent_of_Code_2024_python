import math
import re
import numpy as np
from sympy import Point, Line
# from sympy.utilities.misc import as_int
from sympy.core.numbers import int_valued

lines = []
input_file_name = "test_input_1.txt"
input_file_name = "test_input_2.txt"
# input_file_name = "test_input_3.txt"
# input_file_name = "test_input_4.txt"
# input_file_name = "test_input_5.txt"
input_file_name = "real_input.txt"

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
        # x_target = int(re.findall(r"X=\d+", machine_str)[0][2:])
        x_target = int(re.findall(r"X=\d+", machine_str)[0][2:]) + 10000000000000
        # print(x_target)
        # y_target = int(re.findall(r"Y=\d+", machine_str)[0][2:])
        y_target = int(re.findall(r"Y=\d+", machine_str)[0][2:]) + 10000000000000

        # print(y_target)
        # machine = DotDict({"A_incs": [X_incs[0], Y_incs[0]], "B_incs": [X_incs[1], Y_incs[1]], "target": [x_target, y_target]})
        machine = DotDict({"A_incs": np.array([X_incs[0], Y_incs[0]]), "B_incs": np.array([X_incs[1], Y_incs[1]]), "target": np.array([x_target, y_target])})
        
        # print(machine.A_incs)
        machines.append(machine)

# print(lines)

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

# def isint(i):
#     try: as_int(i, strict=False)
#     except: return False
#     return True

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

    res_1 = target[0]
    res_2 = target[1]

    p1 = Point(0, res_1/b_incs[0])  # Point on first line
    # print(p1)

    p2 = Point(res_1/a_incs[0], 0)  # Another point on first line
    # print(p2)

    p3 = Point(0, res_2/b_incs[1])  # Point on second line
    # print(p3)

    p4 = Point(res_2/a_incs[1], 0)  # Another point on second line
    # print(p4)

    line1 = Line(p1, p2)  # Create first line

    line2 = Line(p3, p4)  # Create second line

    intersection_points = line1.intersection(line2)  # Find intersection
    
    # print(intersection_points)  # Output: [Point2D(1, 1)]
    # print(int(intersection_points[0][0]))  # Output: [Point2D(1, 1)]
    # print(intersection_points[0][0])  # Output: [Point2D(1, 1)]
    # print(isint(intersection_points[0][0]))
    # print(intersection_points[0].x.is_integer)
    # print(int(intersection_points[0][0]) == intersection_points[0][0])
    # print(int_valued(intersection_points[0][0]))

    # if len(intersection_points) > 0 and isint(intersection_points[0][0]) and isint(intersection_points[0][1]):
    if len(intersection_points) > 0:
        mid_a = round(intersection_points[0][0])
        mid_b = round(intersection_points[0][1])
        result = (mid_a * a_incs) + (mid_b * b_incs)
        if np.array_equal(result, target):
            found = True
            print_i(f"\tfound answer: {mid_a} A presses and {mid_b} B presses", 1)
            final_answer += 3 * mid_a + mid_b
            solved_machines.append([a_incs, b_incs, target])
            continue
        else:
            print_i(f"\tdid not find answer: {mid_a} A presses and {mid_b} B presses", 1)
            continue
    else:
        print_i(f"\tdid not find answer: {mid_a} A presses and {mid_b} B presses", 1)
        continue

# print(f"\n\n {solved_machines}")
print(f"\n\n\nsolvable machines: {solvable_machines}") # final answer: 29436
print(final_answer)
# 164803289827454 is too high
# final answer: 103729094227877