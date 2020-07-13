# -*- coding: utf-8 -*-
"""
Created on Sat May 27 23:05:43 2017

@author: SteveShaw
"""

import BondPricing as BP

r=0.06
u=1.25
d=0.9
N=6

future_rates = BP.GetForwardRates(r,u,d,N)
prc_list = BP.CouponBondPricing(future_rates, N, 10, 100, 0.5)
fp_list = BP.BondForwardPricing(future_rates, prc_list[4], 4, 0.5)
z04 = BP.ZeroBondPricing(future_rates,4, 0.5)
fp = fp_list[0]/z04

print(fp)
print(fp_list[0])

combined_forward_rates = BP.GetCombinedForwardRates(r,u,d,11)
eps = BP.ElementaryPrices(combined_forward_rates, 11)
swap_V = BP.ForwardSwapPrcingUsingEP(eps, combined_forward_rates, 0.07, 1, 3)