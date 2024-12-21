import re
lines = []
# input_file_name = "test_input_1.txt"
input_file_name = "test_input_2.txt"
# input_file_name = "test_input_3.txt"
# input_file_name = "real_input.txt"

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

# print(data)
# while True:
for file_index in range(len(data)-1, 0, -1):
    if "." in data[file_index]:
        data[file_index] = ""
    if "." not in data[file_index] and len(data[file_index]) > 0:
        found = False
        for test_file_index in range(file_index, 0, -1):
            if "." in data[test_file_index]:
                found = True
                break
        if found:
            found_file_index = [data[file_index][0]]
            while len(data[file_index]) > 0:
                # print(f"file_index: {file_index} went from {data[file_index][0]} to {data[file_index][:-1]}")
                data[file_index] = data[file_index][:-1]
                found = False
                for test_file_index in range(0, file_index):
                    if "." in data[test_file_index]:
                        data[test_file_index-1] += found_file_index
                        data[test_file_index] = data[test_file_index][:-1]
                        found = True
                        break
                if not found:
                    data[test_file_index-1] += found_file_index

final_answer = 0

print(data)
file_index = 0
for file in data:
    for num in file:
        if num.isalnum():
            print(int(num), end="")
            final_answer += int(num) * file_index
            file_index += 1
print()

# 103893490899 is too low
print(final_answer) # final answer: 6607511583593