# import re

# text = """########
# #..O.O.#
# ##@.O..#
# #...O..#
# #.#.O..#
# #...O..#
# #......#
# ########"""

# pattern = r'^#.*\n#(.*?)#\n(#(.*?)#\n)*#.*$'
# match = re.search(pattern, text, re.MULTILINE | re.DOTALL)
# # print(match)
# print(f"{match.group(0)}\n")

# if match:
#     middle_rows = re.findall(r'#(.*?)#', match.group(0))
#     # print(middle_rows)
#     for row in middle_rows:
#         print(row)

import re

text = """########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########"""

pattern = r'^#.*\n#(.*?)#\n(#(.*?)#\n)*#.*$'
match = re.search(pattern, text, re.MULTILINE | re.DOTALL)

if match:
    middle_rows = re.findall(r'#(.*?)#', match.group(0))
    for row in middle_rows:
        print(row)