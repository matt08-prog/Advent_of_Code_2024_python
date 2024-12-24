from queue import Queue
import re
import threading
lines = []
final_answer = 0
# input_file_name = "test_input_1.txt"
input_file_name = "test_input_2.txt"
input_file_name = "test_input_3.txt"
# input_file_name = "test_input_4.txt"
# input_file_name = "test_input_5.txt"
# input_file_name = "real_input.txt"

# debug = False
debug = True

stones = []
with open(input_file_name) as file:
    col_index = 0
    for line in file:
        stripped_line = line.strip()
        stones_found = re.findall(r"\d+", stripped_line)
        for stone in stones_found:
            stones.append(int(stone))

print(stones)

print()
num_stones = 0

print(f"blink number 0: {stones}")
num_blinks = 6
# num_blinks = 20
num_blinks = 25
# num_blinks = 40
# num_blinks = 75

completed = {}

# def find_in_completed_or_start_new(stone, num_blinks):
#     global completed

#     if stone in completed.keys():


def split_stone(stone, num_blinks, indent=0):
    num_stones = 1

    # print(stone)
    if stone not in completed.keys():
        completed[stone] = []
    # else:
    #     completed[stone].append(stone)

    first_stone = stone
    if indent == 0 and debug:
        print(f"{"\t"*indent}first stone: {first_stone}, {num_blinks} blinks left")

    if num_blinks < 1:
        if debug:
            print(f"{"\t"*indent}stone {first_stone} -> {stone} finished")
        return 1
    for i in range(num_blinks):
        if stone == 0:
            old_stone = stone
            stone = 1
            completed[first_stone].append(stone)
            if debug:
                print(f"{"\t"*indent}({first_stone}): ({old_stone}) -> ({stone}), {num_blinks-i-1} blinks left")
            continue
            # num_stones += 1
        
        stone_str = str(stone)
        stone_len = len(stone_str)
        if stone_len % 2 == 0:
            if debug:
                print(f"{"\t"*indent}({first_stone}): {stone_str[:int(stone_len/2)]} & {stone_str[int(stone_len/2):]} from {stone} with length {stone_len}, {num_blinks-i-1} blinks left")
            new_stone = int(stone_str[int(stone_len/2):])
            # deal with right hand side
            if new_stone in completed.keys():
                new_path = completed[new_stone]
                number_stones_on_path = len(new_path)
                if number_stones_on_path > 0:
                    last_new_path = new_path[-1]
                    if type(last_new_path) is list:
                        # print(f"last new path ({last_new_path}) is a list")
                        last_new_path = new_path[-1][0]
                    # else:
                    #     print(f"last new path ({last_new_path}) is not a list")

                    if num_blinks-i-1-number_stones_on_path < 0 and num_blinks-i-2 > 0:
                        # we have enough blinks to "skip" some of the stones
                        num_stones += num_blinks-i-2
                        if debug:
                            print(f"{"\t"*indent}({first_stone}): skipped ({num_blinks-i-2}) stones; jumped from {new_stone} to {new_path[num_blinks-i-2]} which is element[{num_blinks-i-2}] in {new_path}, num_blinks was {num_blinks-i-1} left. now {0} left")
                        j = 0
                        for testing_stone in new_path[:num_blinks-i-2]: # this is the likely problem
                            if type(testing_stone) is list:
                                print(f"{"\t"*indent}({first_stone}): went through right side of calculated table, element[{j}] of {new_path}")
                                num_stones += split_stone(testing_stone[1], num_blinks-i-2-j, indent + 1)
                            j += 1
                    elif num_blinks-i-2 > 0:
                        # we have enough blinks to "skip" all the stones
                        if debug:
                            print(f"{"\t"*indent}({first_stone}): skipped ({num_blinks-i-2}) stones; jumped from {stone} to end of {new_path}, num_blinks was {num_blinks-i-1} left. now {num_blinks-i-1-number_stones_on_path} left")
                        num_stones += split_stone(last_new_path, num_blinks-i-1-number_stones_on_path, indent + 1)
                        j = 0
                        for testing_stone in new_path:
                            if type(testing_stone) is list:
                                print(f"{"\t"*indent}({first_stone}): went through right side of calculated table, element[{j}] of {new_path}")
                                num_stones += split_stone(testing_stone[1], num_blinks-i-2-j, indent + 1)
                            j += 1
                    else:
                        # this is if we split but we only have one more blinked
                        num_stones += split_stone(new_stone, num_blinks-i-1, indent + 1)
                else:
                    if debug:
                        print(f"{new_stone}'s first split")
                    num_stones += split_stone(new_stone, num_blinks-i-1, indent + 1)
            else:
                if debug:
                    print(f"{new_stone}'s first split")
                num_stones += split_stone(new_stone, num_blinks-i-1, indent + 1)

            # left hand side continues
            stone = int(stone_str[:int(stone_len/2)])
            completed[first_stone].append([stone, new_stone])
            continue
        else:
            old_stone = stone
            stone *= 2024
            if debug:
                print(f"{"\t"*indent}({first_stone}): ({old_stone}) -> ({stone}), {num_blinks-i-1} blinks left")
            completed[first_stone].append(stone)
            # num_stones += 1

    if debug:
        print(f"{"\t"*indent}stone {first_stone} -> {stone} finished")
    return num_stones

# threads = []
# results = Queue()

# Create threads
for stone_index in range(len(stones)):
    stone = stones[stone_index]
    result = split_stone(stone, num_blinks)
    num_stones += result
    print(f"result of {stone} was {result}\n\n")

print()
print(completed)

print("All threads finished")

final_answer = num_stones

print(final_answer) # answer: 185205