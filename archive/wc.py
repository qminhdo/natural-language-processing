import sys
import re

f = open(sys.argv[1], "r")
fl = f.readlines()

types = 0 # unique words
chars = 0
lines = 0
dict = {}

for line in fl:
    lines += 1
    chars += len(line)

    f_line = line.lower()
    f_line = re.sub('[^A-Za-z0-9 ]+', '', f_line)
    f_line = f_line.split(" ")
    for word in f_line:
        dict[word] = dict.get(word, 0) + 1

# Print out result
print("types:" + str(len(dict)), end="")
print(", chars:" + str(chars), end="")
print(", lines:" + str(lines), end=".")