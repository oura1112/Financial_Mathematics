# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 17:16:13 2020

@author: Ryohei Oura
"""

import numpy as np
import matplotlib.pyplot as plt
import math
import copy

class CRR_to_BSM():
    
    def __init__(self):
        self.init_S1 = 100
        self.K = 100
        self.T = 3
        self.r = 0.001
        self.sigma = 0.1
        
    # l and u under risk neutral
    def upper(self,h):
        self.u = self.r * h + self.sigma * np.sqrt(h)
        
    def lower(self,h):
        self.l = self.r * h - self.sigma * np.sqrt(h)
        
    # Put option
    def put_option(self,x):      
        if self.K - x > 0 :
            return self.K - x
        else :
            return 0
    
    # Approximation of phi
    # Note that the function returns phi(-x) directly
    def phi(self,x):
        
        p = 0.2316419
        b1 = 0.31938153
        b2 = -0.356563782
        b3 = 1.781477937
        b4 = -1.821255978
        b5 = 1.330274429
        
        t = 1/(1+p*x)
        
        #return phi(-x)
        return np.exp(-x**2/2)*( b1*t + b2*(t**2) + b3*(t**3) + b4*(t**4) + b5*(t**5) ) / np.sqrt(2*np.pi)
    
    # Define d±
    def d_plusminus(self):
        d_plus = ( np.log(self.init_S1/self.K) + (self.r + self.sigma**2/2)*self.T ) / (self.sigma * np.sqrt(self.T))
        d_minus = ( np.log(self.init_S1/self.K) + (self.r - self.sigma**2/2)*self.T ) / (self.sigma * np.sqrt(self.T))
        
        return d_plus, d_minus
    
    #no arbitrage price on BSM model
    def BSM_price_put(self):
        d_plus, d_minus = self.d_plusminus()
        
        return np.exp(-self.r * self.T) * self.K * self.phi(d_minus) - self.init_S1 * self.phi(d_plus)
    
    #For backward induction, calculate final V in advance
    def final_V(self,N,u,l):
        final_V_list = []

        for i in range(N+1):
            final_S1 = self.init_S1 * (1 + u)**(N-i) * (1 + l)**i
            #print(final_S1)
            final_V = self.put_option(final_S1)
            #print(final_V)
            final_V_list.append(final_V)
            
        return final_V_list
    
    # backward inductive equation
    def backward(self):
        
        N_list = [i for i in range(300) if i%2==1]
        CRR_price_list = []
        BSM_price_list = [self.BSM_price_put()]*len(N_list)
        
        for N in N_list:
            h = self.T/N
            self.upper(h)
            self.lower(h)
            q = 0.5
            
            final_V_list = self.final_V(N,self.u,self.l)
            
            V_list = [final_V_list]
            current_V_list = final_V_list
            
            #calculate xF by back ward inductive equation
            for n in reversed(range(N+1)):
                temporal_V_list = []
                if n > 0:
                    for t in range(n+1):
                        if t > 0:
                            V = ( q * current_V_list[t] + (1-q) * current_V_list[t-1] ) / (1+self.r*h)
                            temporal_V_list.append(V)
                    V_list.append([temporal_V_list])
                    current_V_list = temporal_V_list
            
            no_arbitrage = current_V_list[0]

            CRR_price_list.append(no_arbitrage)
        
        print(BSM_price_list[0])
        plt.plot(N_list, CRR_price_list, label="CRR price")
        plt.plot(N_list, BSM_price_list, label="BSM price")
        plt.legend(loc='upper right')
        plt.xlabel("N")
        plt.ylabel("price")
        plt.show()
        

CRR_to_BSM = CRR_to_BSM()
CRR_to_BSM.backward()        
        