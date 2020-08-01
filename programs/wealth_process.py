# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 16:17:14 2020

@author: oura
"""

import numpy as np
import matplotlib.pyplot as plt
import math

class optimal_wealth_process():
    
    def __init__(self, X_0):
        self.p = 0.6
        self.r = 0.01
        self.u = 0.2
        self.l = -0.2
        self.T = 250
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
            
            #print(X_t_mean_process)
            
        return time, X_t_process, X_t_mean_process        
        
    def sample_plot(self):
        
        time, X_t_process, X_t_mean_process = self.optimal_wealth()
        
        plt.plot(time, X_t_process, label="wealth")
        plt.plot(time, X_t_mean_process, label="mean of wealth")
        plt.legend(loc='upper left')
        plt.xlabel("time")
        plt.ylabel("wealth")
        plt.show()
    
    
    def sample_sd_plot(self):
        
        time, X_t_process, X_t_mean_process = self.optimal_wealth()
        X_t_mean_process = np.array(X_t_mean_process)

        sample_sd = self.calc_sd()
             
        plt.fill_between(time, X_t_mean_process - sample_sd, X_t_mean_process + sample_sd, facecolor='g', alpha=0.2)
        plt.xlabel("time")
        plt.ylabel("standard deviation")
        plt.show()
        
    def calc_sd(self):
        
        N = 30
        sample_collection = []
        
        for i in range(N):
            time, X_t_process, X_t_mean_process = self.optimal_wealth()
            
            sample_collection.append(X_t_process)
            
        sample_collection = np.array(sample_collection)
        
        sample_sd = np.std(sample_collection, axis=0)
        
        return sample_sd
    
        
    def log_process(self):
        
        time = []
        log_process = []
        
        for t in range(self.T):
            if np.random.uniform(0,1) < self.p:
                R_t = self.u
            else:
                R_t = self.l
                
            self.X_t *= ( 1 + (self.R_bar - self.r)*(R_t - self.r) / ( (self.u - self.r)*(self.r - self.l) ) )
            
            time.append(t)
            log_process.append(math.log(self.X_t)/(t+1))
            
        plt.plot(time, log_process)
        plt.legend(loc='upper left')
        plt.xlabel("time")
        plt.ylabel("log_wealth_per_time")
        plt.show()
        print(log_process[-1])

optimal_wealth_process = optimal_wealth_process(X_0=1)

optimal_wealth_process.sample_plot()
#optimal_wealth_process.sample_sd_plot()
#optimal_wealth_process.log_process()
