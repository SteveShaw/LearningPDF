# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np


def vec_midpoint(f, a, b, n):
    h = float(b-a)/n
    x = np.linspace(a+h/2.0, b - h/2.0, n)
    return h * np.sum(f(x))

def vec_trapez(f, a, b, n):
    h = float(b-a)/n
    x = np.linspace(a, b, n+1)
    s = sum(f(x)) - 0.5*f(a) - 0.5*f(b)
    return h*s

def midpint(f, a, b, n):
    h = float(b-a)/n
    result = 0
    for i in range(n):
        result += f((a+h/2.0)+i*h)
    result *= h;
    return result


def MC_double(f, g, x0, y0, x1, y1, n):
    x = np.random.uniform(x0, x1, n)
    y = np.random.uniform(y0, y1, n)
    
    f_mean = 0
    num_inside = 0
    
    for i in range(len(x)):
        for j in range(len(y)):
            if g(x[i], y[j]) >= 0:
                num_inside += 1
                f_mean += f(x[i], y[j])
                
                
    f_mean = f_mean/float(num_inside)
    area = num_inside / float(n**2)*(x1-x0)*(y1-y0)
    return area * f_mean
    

v = lambda t: 3*(t**2)*np.exp(t**3)
print(vec_trapez(v, 0, 1, 10))

def g(x,y):
    return (1 if (0<=x<=2 and 3<=y<=4.5) else -1)
    
print(MC_double(lambda x, y:1, g, 0, 3, 2, 5, 4000))
#==============================================================================
# g = lambda y: math.exp(-y**2)
# 
# n = 1000
# 
# print(midpint(g, 0, 2, n))
#==============================================================================
