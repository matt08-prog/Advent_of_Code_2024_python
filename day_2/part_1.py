floors = []
frequencies = []
similarity_scores = []
# input_file_name = "test_input_1.txt"
input_file_name = "real_input.txt"

num_safe_floors = 0
dir = -1
with open(input_file_name) as file:
    for line in file:
        stripped_line = line.strip().split(" ")
        floors.append([int(i) for i in stripped_line])
        print(floors[-1])
print(floors)

for floor_index in range(len(floors)):
    floor = floors[floor_index]
    level_dir = int(floor[1] - floor[0] > 0) # 0 for down, 1 for up
    num_safe_floors += 1
    for level in range(len(floor) - 1):
        difference = floor[level+1] - floor[level]
        new_level_dir = int(difference > 0) # 0 for down, 1 for up

        if abs(difference) < 1 or abs(difference) > 3 or new_level_dir != level_dir:
            num_safe_floors -= 1
            break

print(num_safe_floors) # answer: 591