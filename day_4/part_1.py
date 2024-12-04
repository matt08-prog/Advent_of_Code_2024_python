import re
lines = []
# input_file_name = "test_input_1.txt"
input_file_name = "real_input.txt"

with open(input_file_name) as file:
    for line in file:
        lines.append(line.strip())
print(lines)

final_answer = 0

def test_word(lines, x, y, test_string="XMAS"):
    # all lines are same length
    dirs = []
    if y >= 3:
        # can look N
        dirs.append([0, -1])
        if x >= 3:
            # can look NW
            dirs.append([-1, -1])
        if len(lines[0]) - 1 - x >= 3:
            # can look NE
            dirs.append([1, -1])
    
    if len(lines[0]) - 1 - x >= 3:
        # can look E
        dirs.append([1, 0])
    if x >= 3:
        # can look W
        dirs.append([-1, 0])

    if len(lines) - 1 - y >= 3:
        # can look S
        dirs.append([0, 1])
        if x >= 3:
            # can look SW
            dirs.append([-1, 1])
        if len(lines[0]) - 1 - x >= 3:
            # can look SE
            dirs.append([1, 1])
    
    final_dirs = dirs.copy()

    for dir in dirs:
        running_x = x
        running_y = y
        for index in range(4):
            running_x = x + dir[0] * index
            running_y = y + dir[1] * index
            if lines[running_y][running_x] != test_string[index]:
                final_dirs.remove(dir)
                break
    
    return len(final_dirs)

num_x_s = 0

for line_index, line in enumerate(lines):
    for letter_index, letter in enumerate(line):
        if letter == "X":
            lines[line_index] = lines[line_index][:letter_index] + "Q" + lines[line_index][letter_index + 1:]
            x = 0
            y = 0

            y_start = max(line_index - 3, 0)
            y_end = min(line_index + 3, len(lines) - 1)
            x_start = max(letter_index - 3, 0)
            x_end = min(letter_index + 3, len(line) - 1)
            lines_to_test = []


            for index in range(y_start, y_end+1):
                # print(f"adding {line[x_start:x_end]} from {line}")
                lines_to_test.append(lines[index][x_start:(x_end+1)])
                print(f"\t{lines_to_test[-1]}")
            
            print(f"found x in:")
            for l_index, l in enumerate(lines_to_test):
                search_index = l.find("Q")
                if search_index != -1:
                    x = search_index
                    y = l_index
                    lines_to_test[l_index] = lines_to_test[l_index][:search_index] + "X" + lines_to_test[l_index][search_index + 1:]
                    break
            

            lines[line_index] = lines[line_index][:letter_index] + "X" + lines[line_index][letter_index + 1:]
            final_answer += test_word(lines_to_test, x, y)
            # break
            num_x_s += 1




print(f"num x's: {num_x_s}")
print(f"final_answer: {final_answer}") # answer: 2562