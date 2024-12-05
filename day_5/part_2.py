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

for update_index, u in enumerate(updates):
    update = updates[update_index].copy()
    passed = True
    for i in range(2): # have to loop twic because sometimes one rule will ruin another
        for rule in rules:
            if rule[0] not in update:
                continue
            if rule[1] not in update:
                continue

            first = update.index(rule[0])
            second = update.index(rule[1])
            
            if first < second:
                # print(f"breaking because {first} < {second}")
                continue

            passed = False
            print(f"testing {update_index} for {rule[0]} < {rule[1]}")
            while first > second:
                print(f"\t update changed from {update} ", end="")
                holder = update.pop(first-1)
                update.insert(first-1, rule[0])
                update.pop(first)
                update.insert(first, holder)
                print(f"to {update}")

                first = update.index(rule[0])
                second = update.index(rule[1])
                # exit(-1)


    if not passed:
        final_answer += update[int(len(update) / 2)]
        print(f"adding {update[int(len(update) / 2)]} from {update_index}")


print(f"final_answer: {final_answer}") # answer: 5346