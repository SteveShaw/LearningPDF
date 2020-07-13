# -*- coding: utf-8 -*-
"""
Created on Sun May 21 18:05:34 2017

@author: SteveShaw
"""

import numpy as np

def BTOption(opt_type,S0, K, r, u, T, N=2000,american="false"):
    #we improve the previous tree by checking for early exercise for american options
   
    #calculate delta T    
    deltaT = float(T) / N
 
    # up and down factor will be constant for the tree so we calculate outside the loop
    u = np.exp(0.3 * np.sqrt(deltaT))
    d = 1.0 / u
 
    #to work with vector we need to init the arrays using numpy
    fs =  np.asarray([0.0 for i in range(N + 1)])
        
    #we need the stock tree for calculations of expiration values
    fs2 = np.asarray([(S0 * u**j * d**(N - j)) for j in range(N + 1)])
    
    #we vectorize the strikes as well so the expiration check will be faster
    fs3 =np.asarray( [float(K) for i in range(N + 1)])
    
 
    #rates are fixed so the probability of up and down are fixed.
    #this is used to make sure the drift is the risk free rate
    a = np.exp(r * deltaT)
    p = (a - d)/ (u - d)
    oneMinusP = 1.0 - p
 
   
    # Compute the leaves, f_{N, j}
    if opt_type =="C":
        fs[:] = np.maximum(fs2-fs3, 0.0)
    else:
        fs[:] = np.maximum(-fs2+fs3, 0.0)
    
   
    #calculate backward the option prices
    for i in range(N-1, -1, -1):
       fs[:-1]=np.exp(-r * deltaT) * (p * fs[1:] + oneMinusP * fs[:-1])
       fs2[:]=fs2[:]*u
      
       if american=='true':
           #Simply check if the option is worth more alive or dead
           if type =="C":
                fs[:]=np.maximum(fs[:],fs2[:]-fs3[:])
           else:
                fs[:]=np.maximum(fs[:],-fs2[:]+fs3[:])
                
    # print fs
    return fs[0]
    
S0 = 100
r=0.02
sigma=0.3
T=0.25
N=15
K = 110

prc = BTOption('C', S0, K, r, sigma, T, N, 'true')
print(prc)