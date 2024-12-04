import re
lines = []
# input_file_name = "test_input_1.txt"
# input_file_name = "test_input_2.txt"
# input_file_name = "test_input_3.txt"
input_file_name = "real_input.txt"

with open(input_file_name) as file:
    for line in file:
        lines.append(line.strip())
print(lines)

final_answer = 0

def test_word(lines, x, y, test_string="MAS"):
    # all lines are same length
    









    if y < 1:
        # can look N
        return 0
    if x < 1:
        # can look NW
        return 0
    # print(f"{len(lines[0])} - 1 - {x} < 0:")
    if len(lines[0]) - 1 - x <= 0:
        # can look NE
        return 0

    if len(lines) - 1 - y <= 0:
        # can look S
        return 0

    NW = lines[y - 1][x - 1]
    NE = lines[y - 1][x + 1]

    SW = lines[y + 1][x - 1]
    SE = lines[y + 1][x + 1]

    if not ((NW == "M" and SE == "S") or (NW == "S" and SE == "M")):
        return 0
    
    if not ((NE == "M" and SW == "S") or (NE == "S" and SW == "M")):
        return 0
    
    return 1

num_a_s = 0

for line_index, line in enumerate(lines):
    for letter_index, letter in enumerate(line):
        if letter == "A":
            lines[line_index] = lines[line_index][:letter_index] + "Q" + lines[line_index][letter_index + 1:]
            x = 0
            y = 0

            y_start = max(line_index - 1, 0)
            y_end = min(line_index + 1, len(lines) - 1)
            x_start = max(letter_index - 1, 0)
            x_end = min(letter_index + 1, len(line) - 1)
            lines_to_test = []


            print(f"found x in:")
            for index in range(y_start, y_end+1):
                # print(f"adding {line[x_start:x_end]} from {line}")
                lines_to_test.append(lines[index][x_start:(x_end+1)])
                print(f"\t{lines_to_test[-1]}")
            
            for l_index, l in enumerate(lines_to_test):
                search_index = l.find("Q")
                if search_index != -1:
                    x = search_index
                    y = l_index
                    lines_to_test[l_index] = lines_to_test[l_index][:search_index] + "A" + lines_to_test[l_index][search_index + 1:]
                    break
            print(f"x ({x}), y ({y})")
            

            lines[line_index] = lines[line_index][:letter_index] + "A" + lines[line_index][letter_index + 1:]
            final_answer += test_word(lines_to_test, x, y)
            # break
            num_a_s += 1




print(f"num a's: {num_a_s}")
print(f"final_answer: {final_answer}") # answer: 1902