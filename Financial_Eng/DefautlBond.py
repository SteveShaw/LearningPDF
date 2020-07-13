# -*- coding: utf-8 -*-
"""
Created on Sat Jun  3 22:49:14 2017

@author: SteveShaw
"""
import numpy as np
import BondPricing as BP

#harzard_lattice = []
r = 0.05
u=1.1
d=0.9
N = 10

def GenHazardRateLattice(nper):
    a=0.01
    b=1.01
    hazard_lattice = [np.array([a])]    
    for i in range(nper):
        t = i+1
        coff = np.arange(t+1) - (t/2)
        #print(coff)
        hazard_lattice.append(a * np.power(b, coff))
        #print(level)
    return hazard_lattice
    
def PricingZCBDefault( rate_lattice, hazard_lattice, face, recovery, pd = 0.5 ):
    price_lattice = []
    price_lattice.append(np.ones_like(rate_lattice[-1])*(1-hazard_lattice[-1])*face) #price at expire
    price_lattice[0] = ( price_lattice[0] + hazard_lattice[-1]*recovery )
    
    
    nper = len(rate_lattice) - 1
    
    r_start = -1
    
    for i in range(nper):
        r_start = r_start - 1
        level_p = np.repeat(price_lattice[0],2)
        level_p = np.delete(level_p, 0)
        level_p = np.delete(level_p, -1)        
        nrows = round(np.size(level_p)/2)
        level_p = np.reshape(level_p, (nrows, 2))
        
        avg_prc = np.average(level_p, axis=1, weights=[pd,1-pd])*(1-hazard_lattice[r_start])
        avg_prc = avg_prc + hazard_lattice[r_start]*recovery
        price_lattice.insert(0, avg_prc/(1.+rate_lattice[r_start]))
    
    return price_lattice
    

rate_lattice = BP.GetCombinedForwardRates(r, u, d, N)    
hr_lattice = GenHazardRateLattice(N)
#print(hr_lattice)
prc_lattice = PricingZCBDefault(rate_lattice, hr_lattice, 100, 20)
print(prc_lattice)

           
            
        
    