# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 16:17:14 2020

@author: oura
"""

import numpy as np
import matplotlib.pyplot as plt

class optimal_wealth_process():
    
    def __init__(self, X_0):
        self.p = 0.6
        self.r = 0.01
        self.u = 0.2
        self.l = -0.2
        self.T = 100
        self.R_bar = self.p * self.u + (1 - self.p) * self.l # = 0.02
        self.X_0 = X_0
        self.X_t = self.X_0
        self.X_t_mean = self.X_0

    def optimal_wealth(self):

        time = []
        X_t_process = []
        X_t_mean_process = []
        
        for t in range(self.T):
            if np.random.uniform(0,1) < self.p:
                R_t = self.u
            else:
                R_t = self.l
                
            self.X_t *= ( 1 + (self.R_bar - self.r)*(R_t - self.r) / ( (self.u - self.r)*(self.r - self.l) ) )
            self.X_t_mean *= ( 1 + (self.R_bar - self.r)**2 / ( (self.u - self.r)*(self.r - self.l) ) )
            
            time.append(t)
            X_t_process.append(self.X_t)
            X_t_mean_process.append(self.X_t_mean)
            
        plt.plot(time, X_t_process, label="wealth")
        plt.plot(time, X_t_mean_process, label="mean of wealth")
        plt.legend(loc='upper left')
        plt.xlabel("time")
        plt.ylabel("wealth")
        plt.show()        

optimal_wealth_process = optimal_wealth_process(X_0=10)

optimal_wealth_process.optimal_wealth()