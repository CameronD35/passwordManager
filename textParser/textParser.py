textFile = open('textparser.txt', 'r')

parsedLines = []

lines = textFile.readlines()

for line in range(0, len(lines)):
    if lines[line] != "\n":
        parsedLines.append(lines[line][:-1])

print(parsedLines)