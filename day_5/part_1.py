import re
# input_file_name = "test_input_1.txt"
input_file_name = "real_input.txt"
rules = []
start_of_updates = 0
updates = []

with open(input_file_name) as file:
    lines = file.readlines()
    
    for line in lines:
        # lines.append(line.strip())
        if line != "\n":
            # print(line[0:2])
            rules.append([int(line[0:2]), int(line[3:5])])
            start_of_updates += 1
        else:
            start_of_updates += 1
            break
    for line in lines[start_of_updates:]:
        stripped_line = line.strip().split(",")
        int_array = [int(i) for i in stripped_line]
        updates.append(int_array)

print(f"rules: {rules}")
print(f"updates: {updates}")

final_answer = 0

for update in updates:
    passed = True
    for rule in rules:
        # print(f"testing {update} for {rule[0]} < {rule[1]}")
        if rule[0] not in update:
            continue
        if rule[1] not in update:
            continue

        first = update.index(rule[0])
        second = update.index(rule[1])
        
        if first > second:
            passed = False
            break

    if passed:
        final_answer += update[int(len(update) / 2)]
        print(update[int(len(update) / 2)])


print(f"final_answer: {final_answer}") # answer: 6260