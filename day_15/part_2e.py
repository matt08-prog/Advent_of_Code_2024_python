from queue import Queue
import re
import threading
lines = []
final_answer = 0
# input_file_name = "test_input_1.txt"
input_file_name = "test_input_2.txt"
input_file_name = "test_input_3.txt"
input_file_name = "test_input_4.txt"
# input_file_name = "test_input_5.txt"
# input_file_name = "real_input.txt"


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
debug = False
debug = True
num_blinks = 6
# num_blinks = 25
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
            if [stone, -1] not in completed[first_stone]:
                completed[first_stone].append([stone, -1])
            if debug:
                print(f"{"\t"*indent}({first_stone}): ({old_stone}) -> ({stone}), {num_blinks-i-1} blinks left")
            continue
            # num_stones += 1
        
        stone_str = str(stone)
        stone_len = len(stone_str)
        if stone_len % 2 == 0:
            if debug:
                print(f"{"\t"*indent}({first_stone}): {stone_str[:int(stone_len/2)]} & {stone_str[int(stone_len/2):]} from {stone} with length {stone_len}, {num_blinks-i-1} blinks left")
            new_stone_l = int(stone_str[:int(stone_len/2)])
            new_stone_r = int(stone_str[int(stone_len/2):])
            # deal with right hand side
            if new_stone_r in completed.keys():
                new_path = completed[new_stone_r]
                number_stones_on_path = len(new_path)
                if number_stones_on_path > 0:
                    # last_new_path = new_path[-1]
                    # if type(last_new_path) is list:
                    #     last_new_path = new_path[-1][0]
                    test_stone_index = 0
                    test_stone = []
                    if num_blinks - i - 2 - test_stone_index < 0:
                        num_stones += split_stone(new_stone_r, num_blinks-i-1, indent + 1)
                    
                    while num_blinks - i - 2 - test_stone_index >= 0:
                        if test_stone_index < number_stones_on_path:
                            # while test_stone_index:
                            test_stone = new_path[test_stone_index]

                            if test_stone[1] != -1:
                                if debug:
                                    print(f"{"\t" * indent}remembered calculated route to the right")
                                # num_stones += 1
                                num_stones += split_stone(test_stone[1], num_blinks-i - 2 - test_stone_index, indent + 1)
                            test_stone_index += 1
                        else:
                            # if test_stone == new_path[-1]:
                            #     completed[new_stone_r].append(test_stone)
                            num_stones += split_stone(test_stone[0], num_blinks- i - 1 - test_stone_index, indent + 1)
                            break

                    # if len(test_stone) > 0 :
                        # num_stones += split_stone(test_stone[0], num_blinks- i - 2 - test_stone_index, indent + 1)
                    
                else:
                    # if debug:
                    #     # print(f"{new_stone}'s first split")
                    num_stones += split_stone(new_stone_r, num_blinks-i-1, indent + 1)
                    # completed[new_stone_r].append([new_stone_l, new_stone_r])
            else:
                # if debug:
                    # print(f"{new_stone}'s first split")
                num_stones += split_stone(new_stone_r, num_blinks-i-1, indent + 1)
                print(f"{[new_stone_l, new_stone_r]} comes after {stone}")
                # completed[new_stone_r] = [[new_stone_l, new_stone_r]]

            # left hand side continues
            if [new_stone_l, new_stone_r] not in completed[first_stone]:
                if [new_stone_l, new_stone_r] == [2024, -1]:
                    print(f"--------------------------------{[new_stone_l, new_stone_r]} is not in {completed[first_stone]}")
                completed[first_stone].append([new_stone_l, new_stone_r])
            stone = new_stone_l
            continue
        else:
            old_stone = stone
            stone *= 2024
            if debug:
                print(f"{"\t"*indent}({first_stone}): ({old_stone}) -> ({stone}), {num_blinks-i-1} blinks left")
            if [stone, -1] not in completed[first_stone]:
                completed[first_stone].append([stone, -1])
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