# -*- coding: utf-8 -*-
"""
Created on Sat Sep  9 18:53:50 2017

@author: SteveShaw
"""

import midpoint

def test_midpoint():
    import math
    v = lambda t: 3*(t**2)*math.exp(t**3)
    n = 1000
    computed = midpoint.midpint(v, 0.0, 1.0, n)
    print(computed)
    expected =  2.463642041244344
    error = abs(expected - computed)
    tol = 1E-14
    success = error < tol
    msg = 'error=%g > tol=%g'%(error, tol)
    assert success, msg
    
test_midpoint()