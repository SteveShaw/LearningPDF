# -*- coding: utf-8 -*-
"""
Created on Sun Sep 10 22:25:25 2017

@author: SteveShaw
"""

import numpy as np
import matplotlib.pyplot as plt

def ode_FE(f, init, delta_t, T):
    N_t = int(round(float(T)/delta_t))
    u = np.zeros(N_t+1)
    t = np.linspace(0, N_t*delta_t, len(u))
    u[0] = init
    for n in range(N_t):
        u[n+1] = u[n] + delta_t*f(u[n], t[n])
    return u, t

def demo_population_growth():
    def f(u,t):
        return 0.1*u
    
    u, t = ode_FE(f=f, init=100, delta_t=0.5, T=20)
    plt.plot(t, u, t, 100*np.exp(0.1*t))
    plt.show()
    

def demo_logistic():
    for dt, T in zip((0.5, 20), (60, 100)):
        u, t = ode_FE(f=lambda u, t: 0.1*(1-u/500.)*u,
                  init=100, delta_t=dt, T=T)
        plt.figure()
        plt.plot(t, u, 'b-')
        plt.xlabel('t'); plt.ylabel('N(t)')
        plt.savefig('tmp_%g.png'%dt)
    
if __name__=='__main__':
    #demo_population_growth()
    demo_logistic()