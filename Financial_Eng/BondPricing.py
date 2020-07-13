# -*- coding: utf-8 -*-
"""
Created on Sat May 27 23:04:58 2017

@author: SteveShaw
"""

import numpy as np

#get forward rates
#return a list
def GetForwardRates(r, u, d, N):
    pa = np.array([u,d])
    r_list = []
    r_list.append(r)
    for i in range(N):
        r = np.outer(r_list[-1], pa)
        r_list.append(r.flatten())

    return r_list

def ZeroBondPricing(rates,ex,p):
    t_start = ex-1
    PN = 100/(1.0+rates[t_start])
    if ex < 1:
        return PN
    for i in range(t_start):
        t = t_start-1-i
        P = np.reshape(PN,(int(PN.shape[0]/2),2)) #change the arrays into a nx2 matrix so that each row can be treated efficiently
        avg_prob_prc = np.average(P, axis=1, weights=[p,1-p])
        PN = avg_prob_prc/(1.0+rates[t])
        #PN = np.mean(P, axis=1)
    return PN

def CouponBondPricing(rates,ex,coupon,face,p):
    t_start = ex-1
    price_list=[]
    price_list.append((face+coupon)/(1.0+rates[t_start]))
    
    if ex > 1:
        for i in range(t_start):
            t = t_start-1-i
            P = np.reshape(price_list[0],(int(price_list[0].shape[0]/2),2)) #change the arrays into a nx2 matrix so that each row can be treated efficiently
            avg_prob_prc = np.average(P, axis=1, weights=[p,1-p])
            price_list.insert(0, (avg_prob_prc+coupon)/(1.0+rates[t]))
            #PN = np.mean(P, axis=1)
    return price_list  #notice: this list does not include coupon, when getting real price, need to add coupon

def BondForwardPricing(rates, bond_prc_at_forward_expire, expire, p, is_future=False):
    fp_list = []
    fp_list.append( bond_prc_at_forward_expire )
    for i in range(expire):
        t = expire - 1- i
        P = np.reshape(fp_list[0], (int(fp_list[0].shape[0]/2),2))
        avg_prob_prc = np.average(P, axis=1, weights=[p,1-p])
        if not is_future:
            fp_list.insert(0, avg_prob_prc/(1.0+rates[t]))
        else:
            fp_list.insert(0, avg_prob_prc)
    return fp_list
    
def BondOptionPricing(bond_prcs, rates, strike, expire, opt_type=1, European=True, p=0.5):
    zeros = np.zeros(bond_prcs[expire].shape)
    opt_prc_ls = []
    opt_prc_ls.append( np.maximum(opt_type*(bond_prcs[expire]-strike), zeros) )
    
    if European:
        for i in range(expire):
            t = expire - 1 - i
            P = np.reshape(opt_prc_ls[0], (int(opt_prc_ls[0].shape[0]/2),2))
            avg_prob_prc = np.average(P, axis=1, weights=[p,1-p])
            opt_prc_ls.insert(0, avg_prob_prc/(1.0+rates[t]))
    else:
        for i in range(expire):
            t = expire - 1 - i
            P = np.reshape(opt_prc_ls[0], (int(opt_prc_ls[0].shape[0]/2),2))
            avg_prob_prc = np.average(P, axis=1, weights=[p,1-p])
            prc_strike_diff = np.maximum(opt_type*(bond_prcs[t]-strike), zeros[:avg_prob_prc.shape[0]])
            opt_prc_ls.insert(0, np.maximum( avg_prob_prc/(1.0+rates[t]), prc_strike_diff) )
            
    return opt_prc_ls

#combine the same rates    
def GetCombinedForwardRates(r, u, d, N):
    pa = np.array([u,d])
    r_list = []
    r_list.append(r)
    for i in range(N):
        r = np.outer(r_list[-1], pa)
        r = r.flatten()
        r = np.insert(r,0,r[0])
        r = np.append(r,r[-1])
        rows = int(r.shape[0]/2)
        r = np.reshape(r,(rows,2))
        r = np.mean(r, axis=1)
        r_list.append(r.flatten())

    return r_list
    
def ElementaryPrices(combined_rates, N):
    ep_ls = []
    ep_ls.append(np.array([1]))
    for t in range(N):
        prc_t = np.repeat(ep_ls[-1],2)
        prc_t = np.insert(prc_t,0,0)
        prc_t = np.append(prc_t,0)
        
        r_t = np.repeat(combined_rates[t], 2)
        r_t = np.insert(r_t,0,0)
        r_t = np.append(r_t,0)
        
        pv = prc_t/(1+r_t)*0.5
        rows = int(pv.shape[0]/2)
        pv = np.reshape(pv, (rows,2))
        ep_ls.append(np.sum(pv, axis=1))
    return ep_ls
    
def ForwardSwapPrcingUsingEP( elem_prices, combined_rates, fixed_rate, start, end ):
    V0 = 0
    for t in range(start, end):
        coff = ( fixed_rate - combined_rates[t] ) / (1+combined_rates[t])
        Vt = np.sum(coff*elem_prices[t])
        V0 = V0 + Vt
    return V0
        