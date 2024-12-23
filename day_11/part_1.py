import re
lines = []
final_answer = 0
input_file_name = "test_input_1.txt"
input_file_name = "test_input_2.txt"
# input_file_name = "test_input_3.txt"
# input_file_name = "test_input_4.txt"
# input_file_name = "test_input_5.txt"
input_file_name = "real_input.txt"

# def test_letter(x, y):
#     if y >= 0 and y < num_rows and x >= 0 and x < num_cols:
#         return True
#     return False

stones = []
with open(input_file_name) as file:
    col_index = 0
    for line in file:
        stripped_line = line.strip()
        stones = re.findall(r"\d+", stripped_line)

print(stones)

print()
num_stones = len(stones)

print(f"blink number 0: {stones}")
num_blinks = 25
for i in range(num_blinks):
    stone_index = 0
    while stone_index < num_stones:
    # for stone_index in range(0, num_stones):
        stone = stones[stone_index]
        if stone == "0":
            stones[stone_index] = "1"
            stone_index += 1
            continue

        stone_len = len(stone)
        if stone_len % 2 == 0:
            stones[stone_index] = stone[:int(stone_len/2)]
            stones.insert(stone_index + 1, str(int(stone[int(stone_len/2):])))
            num_stones += 1
            stone_index += 2
            continue

        # otherwise
        stones[stone_index] = str(int(stone) * 2024)
        stone_index += 1
    print(f"blink number {i}: {stones}")

num_stones = len(stones)
final_answer = num_stones

print(final_answer) # answer: 185205