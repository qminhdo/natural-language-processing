# String is immutable
# tuple is immutable
# list is mutable

import sys
import re

# reading args when running from command line


# Using RegEx
string = "I want to go to Boston"
r = re.match('(I|We) want to go to (Boston|Chicago)', string)
print(r)

# Using map
l = [2,4,6,1]
newl = [x**x for x in l]
print(newl)

# Using print
print("==============")
print("Using Print")
x = min(3,4)
print("x = ", x, sep = "")

# Casting
x = 3.5
x = int(3.5)
x = float(x)
# Power
x = 2**3

# integer division
x = 3//4

# Using input
print("==============")
print("Using Input")
# x = input()
# print("You entered:", x)
# or
# x = float(input("Enter a number"))

# Using List
print("==============")
print("Using List")
list = [1,2,3]
print(list)

list = []
list.append("Dog")
list.append("Cat")
list.insert(1,"Bird")

print(list)
print("Length:", len(list))
print("Index 1:", list[1])

del(list[1:3])
print(list)

list2 = []
list2.append("Mouse")
list2.append("Mice")

list.extend(list2)
print(list)

list3 = list + list2
print(list3)

# add a list to a list
list3.append(list)
list3.append(list2)
print(list3)
# access list[1] from list3
print(list3[6][1])

list3[0] = 4
print(list3)

# Immutable tupple
# List that cannot be modified
print("==============")
print("Using Immutable tupple")
# tupple can contain object
x = "house"
print(x)

x = 2, 3, 4, 5
print(x)

print(7 in x) # return false

# tuple within tuple
y = x, 5, "yes"
print(y)
print(y[0])
print(y[1:])
print(len(y))
print(len(y[0]))

# Using Substring
print("==============")
print("Using Substring")
s = "input"
print("Length:", len(s))
print("Substring from index 2:", s[2: ])
print("Substring from index 1-3(exclusive):", s[1:3])
print("Substring from starting last 3 to last 1:", s[-3: -1])

# Using Search
print("==============")
print("Using Search")
s = "input"
print("Contains:", ("pue" in s))


# Using comparision
print("==============")
print("Using comparision")

# Comparing number
# not, and, or
# ==, !=, <, >, <=, >=
x = 4
y = 5
print(x == y) # false
print(4 != 5) # true
print(not (4 < 5)) # false
print(4 < 5 and 6 < 7)

# comparing string
x = "dog"
y = "cat"
print(x is y)  # false
y = "dog"
print(x is y) # true

# Using if statement
print("==============")
print("Using If statement")
# use colon after if statement
if 4 < 5:
    print("it is true")

if 4 > 5:
    print("it is true")
elif 5 > 7:
    print("hah")
else:
    print("it is false") # print this

# Using loop
print("==============")
print("Using loop")

x = 0
while x < 5:
    # for space, without it, it will print new line
    print(x, end = " ") # 0 1 2 3 4
    x+=1

print()
# for (int i = 0; i <5; i++)
# loop start from index 0
# 0 1 2 3 4
for x in range(5):
    print(x, end = " ") # 0 1 2 3 4

print()
# from 2 to 10, increase by 3 each time
for x in range(2, 10, 3):
    print(x, end = " ") # 2 5 8
print()

# foreach loop
list = [1,2,3,4]
for x in list:
    if x == 3:
        break
        # continue
    print(x, end=" ")
print()


# combine an else statement with repetition statement
for x in range(5):
    if x == 6:
        break
else:
    print("entered else")  # entered else


# define method
print("==============")
print("Define method")

def sum(a,b,c):
    return a + b + c

mystery = sum
print(sum(1,2,3))
print(mystery(1,2,3))

# optional param without create new def
# default for c is 0 if user doesnt enter c
def sum(a,b,c = 0):
    return a + b + c

# Creating class / object
print("==============")
print("Creating object")

# moduel name doesnt have to be same as class name
class Dog:
    # constructor
    def __init__(self, name, age):
        # underscore is private variable
        self._name = name;
        self._age = age


    def get_age(self):
        return self._age
    def get_name(self):
        return self._name
    def set_name(self, name):
        self._name = name

    # toString() method in python
    def __str__(self):
        return "Dog:\nName: " + self._name + " " + str(self._age)

    # without self, it will be class method
    def random():
        return 7

d1 = Dog("Mike", 5)
print(d1)
print(d1.get_name())
print(Dog.random())

