from queue import Queue
import re
import threading


def split_stone(stone, num_blinks, results):
    num_stones = 1
    my_results = Queue()
    threads = []

    if num_blinks < 1:
        results.put(1)
        return
    for i in range(num_blinks):
        stone_len = len(stone)
        if stone == "0":
            stone = "1"
        elif stone_len % 2 == 0:
            # print(f"{stone[:int(stone_len/2)]} & {stone[int(stone_len/2):]} from {stone} with length {stone_len}, {num_blinks-i-1} blinks left")
            new_stone = str(int(stone[int(stone_len/2):]))
            thread = threading.Thread(target=split_stone, args=(new_stone, num_blinks-i-1, my_results))
            threads.append(thread)
            thread.start()
            for thread in threads:
                thread.join()
            stone = stone[:int(stone_len/2)]
        else:
            stone = str(int(stone) * 2024)

    while not my_results.empty():
        num_stones += my_results.get()
    results.put(num_stones)

if __name__=="__main__": 
    lines = []
    final_answer = 0
    # input_file_name = "test_input_1.txt"
    input_file_name = "test_input_2.txt"
    # input_file_name = "test_input_3.txt"
    # input_file_name = "test_input_4.txt"
    # input_file_name = "test_input_5.txt"
    # input_file_name = "real_input.txt"

    stones = []
    with open(input_file_name) as file:
        col_index = 0
        for line in file:
            stripped_line = line.strip()
            stones = re.findall(r"\d+", stripped_line)

    print(stones)

    print()
    num_stones = len(stones)

    print(f"blink number 0: {stones}")
    num_blinks = 6
    # num_blinks = 20
    num_blinks = 25
    # num_blinks = 75
    threads = []
    results = Queue()
    # Create threads
    for stone_index in range(len(stones)):
        stone = stones[stone_index]
        thread = threading.Thread(target=split_stone, args=(stone, num_blinks, results))
        threads.append(thread)
        thread.start()

    for thread in threads:
        # Wait for threads to finish
        thread.join()

    print("All threads finished")

    # num_stones = len(stones)
    while not results.empty():
        final_answer += results.get()
    # final_answer = num_stones

    print(final_answer) # answer: 185205

