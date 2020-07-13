# -*- coding: utf-8 -*-
"""
Created on Sun Sep 10 19:37:32 2017

@author: SteveShaw
"""

import numpy as np

def get_pi(N):
    pi_ = 0
    k = np.linspace(0, N, N+1)
    pi_ = np.sum(8.0/(4.0*k+1)*1.0/(4.0*k+3))
    return pi_

print(get_pi(9000000))

