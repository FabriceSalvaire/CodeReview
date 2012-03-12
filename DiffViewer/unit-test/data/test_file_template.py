""" This is a Python Module
"""

import os
import sys

def function1(x, y):
    """ This is function 1 """
    x += 1
    y += 2
    return x + y

list1 = [x + 1
         for x in xrange(10)]

z = function1(1, 2)

print "Hello World!"

def function2(x):
    """ This is function 2 """
    a = 1
    b = 2
    return a * x + b

var1 = function2(10)
var2 = function2(20)
    
# this is the End
