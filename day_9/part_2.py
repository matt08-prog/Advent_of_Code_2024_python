import re
lines = []
input_file_name = "test_input_1.txt"
input_file_name = "test_input_2.txt"
input_file_name = "test_input_3.txt"
input_file_name = "real_input.txt"

with open(input_file_name) as file:
    for line in file:
        lines.append(line)
# print(lines)

mul_results_sum = 0
data = []

for line in lines:
    blocks = re.findall(r"\d", line)
    file_index = 0
    # print(blocks)
    for block in blocks:
        if file_index % 2 == 0:
            data.append([str(int(file_index/2))] * int(block))
        else:
            data.append("." * int(block))
        file_index += 1
        # print(data[-1])

for d in data:
    print(d, end="")
print("\n")

# for file in data:
#     for num in file:
#         if num.isalnum():
#             print(int(num), end="")
#             # final_answer += int(num) * file_index
#         else:
#             print(num, end="")
# # print()
print(data)
print("\n")

# while True:
for file_index in range(len(data)-1, 0, -1):
    # if "." in data[file_index]:
    #     data[file_index] = ""
    if "." not in data[file_index] and len(data[file_index]) > 0:
        found = False
        for test_file_index in range(file_index, 0, -1):
            if "." in data[test_file_index]:
                found = True
                break
        if found:
            found_file_index = [data[file_index][0]]
            file_length = len(data[file_index])
            while len(data[file_index]) > 0:
                found_right_hole = False
                found_hole = False
                for test_file_index in range(0, file_index):
                    if "." in data[test_file_index]:
                        found_hole = True
                        if len(data[test_file_index]) >= file_length:
                            # print(f"\tlength of file: {file_length}, length of gap: {len(data[test_file_index])}")
                            # data[test_file_index-1] += found_file_index * file_length
                            data.insert(test_file_index, found_file_index * file_length)
                            # data[test_file_index] = data[test_file_index][:-1]
                            data[test_file_index+1] = "." * (len(data[test_file_index+1]) - file_length)
                            found_right_hole = True
                            break
                        # else:
                        #     print(f"\t{data[file_index]} won't fit in {data[test_file_index]}")
                if found_right_hole:
                    # print(f"file_index: {file_index} went from {data[file_index][0]} to {data[file_index][:-1]}")
                    
                    data[file_index+1] = "." * file_length
                    # for file in data:
                    #     for num in file:
                    #         if num.isalnum():
                    #             print(int(num), end="")
                    #             # final_answer += int(num) * file_index
                    #         else:
                    #             print(num, end="")
                    # print()

                    # print(data)
                    # print("\n")
                if found_hole:
                #     data[test_file_index-1] += found_file_index
                    break

final_answer = 0

# print(data)
file_index = 0
for file in data:
    for num in file:
        if num.isalnum():
            print(int(num), end="")
            final_answer += int(num) * file_index
        else:
            print(num, end="")
        file_index += 1

print()

print(final_answer) # final answer: 6636608781232