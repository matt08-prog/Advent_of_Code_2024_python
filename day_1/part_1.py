left_list = []
right_list = []
differences = []
with open("real_input.txt") as file:
    for line in file:
        stripped_line = " ".join(line.split()).split(" ")
        print(stripped_line)
        left_list.append(int(stripped_line[0]))
        right_list.append(int(stripped_line[1]))

left_list.sort()
right_list.sort()
print(left_list)
print(right_list)
for i in range(len(left_list)):
    differences.append(abs(left_list[i] - right_list[i]))

print(differences)
print(sum(differences)) # answer: 1151792