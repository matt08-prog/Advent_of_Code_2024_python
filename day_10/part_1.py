import re
lines = []
# input_file_name = "test_input_1.txt"
# input_file_name = "test_input_2.txt"
# input_file_name = "test_input_3.txt"
# input_file_name = "test_input_4.txt"
# input_file_name = "test_input_5.txt"
input_file_name = "real_input.txt"

def test_letter(x, y):
    if y >= 0 and y < num_rows and x >= 0 and x < num_cols:
        return True
    return False

trailheads = []
with open(input_file_name) as file:
    col_index = 0
    for line in file:
        for char_index in range(len(line)):
            if line[char_index] == "0":
                trailheads.append([char_index, col_index, 0, [char_index, col_index]])
        lines.append(line.strip())
        col_index += 1

print(lines)

print()

print(trailheads)

num_rows = len(lines)
num_cols = len(lines[0])

mul_results_sum = 0
data = []

final_answer = 0

dirs = [[1, 0], [0, 1], [-1, 0], [0, -1]]
ends = []

num_trailheads = len(trailheads)
trailhead_index = 0

print(f"trailheads: {trailheads}")

while (trailhead_index < num_trailheads):
    head = trailheads[trailhead_index]
    print(f"testing trailhead #{trailhead_index}: {head}")
    # last_num = 0
    for dir in dirs:
        test_pos = [head[0] + dir[0], head[1] + dir[1]]
        if test_letter(test_pos[0], test_pos[1]):
            test_char = lines[test_pos[1]][test_pos[0]]
            # if test_char.isalnum():
            if True:
                if int(test_char) == head[2] + 1:
                    if [test_pos[0], test_pos[1], int(test_char)] not in trailheads:
                        trailheads.append([test_pos[0], test_pos[1], int(test_char), head[3]])
                        num_trailheads += 1
                    if int(test_char) == 9 and [test_pos, head[3]] not in ends:
                        final_answer += 1
                        ends.append([test_pos, head[3]])
    trailhead_index += 1


print(final_answer) # answer: 782