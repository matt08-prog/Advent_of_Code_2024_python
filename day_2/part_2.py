def check_if_floor_is_safe(floor):
    level_dir = int(floor[1] - floor[0] > 0) # 0 for down, 1 for up

    for level in range(len(floor) - 1):
        difference = floor[level+1] - floor[level]
        new_level_dir = int(difference > 0) # 0 for down, 1 for up

        if abs(difference) < 1 or abs(difference) > 3 or new_level_dir != level_dir:
            print(f"\t unsafe subfloor {floor}")
            return 1
    print(f"\t safe subfloor {floor}")
    return 0


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
    # num_safe_floors += 1
    num_unsafe_levels = 0
    print(f"from floor: {floor}")
    if check_if_floor_is_safe(floor) == 0:
        num_safe_floors += 1
        continue

    for sub_floor_index in range(0, len(floor)):
        if check_if_floor_is_safe([element for i, element in enumerate(floor) if i != sub_floor_index]) == 0:
            num_safe_floors += 1
            break
    # if num_unsafe_levels < 2:
    #     num_safe_floors += 1

print(num_safe_floors) # answer: 621