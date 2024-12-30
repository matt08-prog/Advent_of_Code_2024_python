# coding=utf8
# the above tag defines encoding for this document and is for Python 2.x compatibility

import re

# regex = r"\n#(#+[^#]+|[^#]+|[^#]+#[^#]+)#$|([<^>v]+)" # works for test data
# regex = r"\n#((?:[^#]+#+[^#]+){1,}|(?:[^#]+#+[^#]+){1,}#+|#+(?:[^#]+#+[^#]+){1,}#+|#+(?:[^#]+#+[^#]+){1,}|(?:[^#]+#+[^#]+#+[^#]+){1,})#$|([<^>v]+)"
regex = r"\n#((#*(?:[^#]+#+(?!$)){1,}[^#]*))|([<^>v]+)" # works for real data
regex = r"\n#(?:(#*(?:[^#]+#+(?!$)){1,}[^#]*))|([<^>v]+)" # works for real data (only 2 groups)
regex = r"\n#(?:(#*(?:[^#]+#+(?!$)){1,}[^#]*|[^#]+))|([<^>v]+)" # works for real data and test_input_2
regex = r"\n#(?:(#*(?:[^#]+#+(?!$)){1,}[^#]*|[^#]+|#+(?!$)[^#]+))|([<^>v]+)" # works for real data and all test_inputs

test_str = ("########\n"
	"#..O.O.#\n"
	"##@.O..#\n"
	"#...O..#\n"
	"#.#.O..#\n"
	"#...O..#\n"
	"#......#\n"
	"########\n\n"
	"<^^>>>vv<v>>v<<")

matches = re.finditer(regex, test_str, re.MULTILINE)

for matchNum, match in enumerate(matches, start=1):
    
    # print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
    
    for groupNum in range(0, len(match.groups())):
        groupNum = groupNum + 1
        
        print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))

# Note: for Python 2.7 compatibility, use ur"" to prefix the regex and u"" to prefix the test string and substitution.
