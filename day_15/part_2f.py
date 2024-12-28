from queue import Queue
import re
import threading
lines = []
final_answer = 0
# input_file_name = "test_input_1.txt"
input_file_name = "test_input_2.txt"
# input_file_name = "test_input_3.txt"
# input_file_name = "test_input_4.txt"
# input_file_name = "test_input_5.txt"
input_file_name = "real_input.txt"

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
num_blinks = 75

completed = {}

def split_stone(stone, num_blinks, indent=0):
    global completed

    num_stones = 0

        
    # else:
    #     completed[stone].append(stone)

    # first_stone = stone
    # if indent == 0:
    #     print(f"{"\t"*indent}first stone: {first_stone}, {num_blinks} blinks left")

    if num_blinks < 1:
        # print(f"{"\t"*indent}stone {first_stone} -> {stone} finished")
        return 1
    for i in range(num_blinks):
        if stone in completed.keys():
            found = completed[stone]
            if len(found) == 2:
                num_stones += split_stone(found[1], num_blinks-i-1, indent + 1)
            num_stones += split_stone(found[0], num_blinks-i-1, indent + 1)
            return num_stones
        if stone == 0:
            old_stone = stone
            stone = 1
            completed[0] = [1]

            # print(f"{"\t"*indent}({first_stone}): ({old_stone}) -> ({stone}), {num_blinks-i-1} blinks left")
            continue
        
        stone_str = str(stone)
        stone_len = len(stone_str)
        if stone_len % 2 == 0:
            old_stone = stone
            # print(f"{"\t"*indent}({first_stone}): {stone_str[:int(stone_len/2)]} & {stone_str[int(stone_len/2):]} from {stone} with length {stone_len}, {num_blinks-i-1} blinks left")
            new_stone = int(stone_str[int(stone_len/2):])

            num_stones += split_stone(new_stone, num_blinks-i-1, indent + 1)

            # left hand side continues
            stone = int(stone_str[:int(stone_len/2)])
            completed[old_stone] = [stone, new_stone]
            continue
        else:
            old_stone = stone
            # stone *= 2024
            result = stone * 2024
            stone = result
            # print(f"{"\t"*indent}({first_stone}): ({old_stone}) -> ({stone}), {num_blinks-i-1} blinks left")
            # num_stones += split_stone(result, num_blinks-i-1, indent + 1)
            
            completed[old_stone] = [result]
            # num_stones += 1

    # print(f"{"\t"*indent}stone {first_stone} -> {stone} finished")
    return num_stones + 1

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