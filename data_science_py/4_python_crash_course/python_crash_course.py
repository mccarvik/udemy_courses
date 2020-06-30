#!/usr/bin/env python
# coding: utf-8

# ___
# 
# <a href='http://www.pieriandata.com'> <img src='../Pierian_Data_Logo.png' /></a>
# ___
# # Python Crash Course
# 
# Please note, this is not meant to be a comprehensive overview of Python or programming in general, if you have no programming experience, you should probably take my other course: [Complete Python Bootcamp](https://www.udemy.com/complete-python-bootcamp/?couponCode=PY20) instead.
# 
# **This notebook is just a code reference for the videos, no written explanations here**
# 
# This notebook will just go through the basic topics in order:
# 
# * Data types
#     * Numbers
#     * Strings
#     * Printing
#     * Lists
#     * Dictionaries
#     * Booleans
#     * Tuples 
#     * Sets
# * Comparison Operators
# * if, elif, else Statements
# * for Loops
# * while Loops
# * range()
# * list comprehension
# * functions
# * lambda expressions
# * map and filter
# * methods
# ____
import sys

# ## Data types
# 
# ### Numbers

print(1 + 1)
print(1 * 3)
print(1 / 2)
print(2 ** 4)
print(4 % 2)
print(5 % 2)
print((2 + 3) * (5 + 5))

# ### Variable Assignment
# Can not start with number or special characters
name_of_var = 2

x = 2
y = 3
z = x + y
print(z)

# ### Strings
print('single quotes')
print("double quotes")
print(" wrap lot's of other quotes")

# ### Printing
x = 'hello'
print(x)
num = 12
name = 'Sam'
print('My number is: {one}, and my name is: {two}'.format(one=num,two=name))
print('My number is: {}, and my name is: {}'.format(num, name))

# ### Lists
print([1,2,3])
print(['hi',1,[1,2]])
my_list = ['a','b','c']
my_list.append('d')
print(my_list)
print(my_list[0])
print(my_list[1])
print(my_list[1:])
print(my_list[:1])
my_list[0] = 'NEW'
print(my_list)
nest = [1,2,3,[4,5,['target']]]
print(nest[3])
print(nest[3][2])
print(nest[3][2][0])


# ### Dictionaries
d = {'key1':'item1','key2':'item2'}
print(d)
print(d['key1'])

# ### Booleans
print(True)
print(False)

# ### Tuples 
t = (1,2,3)
print(t[0])
# will give an error
# t[0] = 'NEW'

# ### Sets
print({1,2,3})
print({1,2,3,1,2,1,2,3,3,3,3,2,2,2,1,1,2})

# ## Comparison Operators
print(1 > 2)
print(1 < 2)
print(1 >= 1)
print(1 <= 4)
print(1 == 1)
print('hi' == 'bye')

# ## Logic Operators
print((1 > 2) and (2 < 3))
print((1 > 2) or (2 < 3))
print((1 == 2) or (2 == 3) or (4 == 4))

# ## if,elif, else Statements
if 1 < 2:
    print('Yep!')

if 1 < 2:
    print('yep!')

if 1 < 2:
    print('first')
else:
    print('last')

if 1 > 2:
    print('first')
else:
    print('last')

if 1 == 2:
    print('first')
elif 3 == 3:
    print('middle')
else:
    print('Last')

# ## for Loops
seq = [1,2,3,4,5]
for item in seq:
    print(item)

for item in seq:
    print('Yep')

for jelly in seq:
    print(jelly+jelly)

# ## while Loops
i = 1
while i < 5:
    print('i is: {}'.format(i))
    i = i+1

# ## range()
print(range(5))
for i in range(5):
    print(i)
print(list(range(5)))

# ## list comprehension
x = [1,2,3,4]
out = []
for item in x:
    out.append(item**2)
print(out)

print([item**2 for item in x])

# ## functions
def my_func(param1='default'):
    """
    Docstring goes here.
    """
    print(param1)

print(my_func)
my_func()
my_func('new param')
my_func(param1='new param')

def square(x):
    return x**2

out = square(2)
print(out)

# ## lambda expressions
def times2(var):
    return var*2

print(times2(2))
print(lambda var: var*2)

# ## map and filter
seq = [1,2,3,4,5]
print(map(times2,seq))
print(list(map(times2,seq)))
print(list(map(lambda var: var*2,seq)))
print(filter(lambda item: item%2 == 0,seq))
print(list(filter(lambda item: item%2 == 0,seq)))

# ## methods
st = 'hello my name is Sam'
print(st.lower())
print(st.upper())
print(st.split())
tweet = 'Go Sports! #Sports'
print(tweet.split('#'))
print(tweet.split('#')[1])

print(d)
print(d.keys())
print(d.items())
print(d.values())
lst = [1,2,3]
print(lst.pop())
print(lst)
print('x' in [1,2,3])
print('x' in ['x','y','z'])
