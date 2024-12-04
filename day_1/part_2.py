left_list = []
right_list = []
frequencies = []
similarity_scores = []
# input_file_name = "test_input_1.txt"
input_file_name = "real_input.txt"

with open(input_file_name) as file:
    for line in file:
        stripped_line = " ".join(line.split()).split(" ")
        print(stripped_line)
        left_list.append(int(stripped_line[0]))
        right_list.append(int(stripped_line[1]))

left_list.sort()
right_list.sort()
print(left_list)
print(right_list)


for i in range(max(left_list) + 1):
    frequencies.append(right_list.count(i))

for i in range(len(left_list)):
    similarity_scores.append(left_list[i] * frequencies[left_list[i]])

print(similarity_scores)
print(sum(similarity_scores)) # answer: 21790168