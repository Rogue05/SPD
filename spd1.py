# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 20:04:48 2019

@author: Wojtek
"""

class proc:
    def __init__(self,uid,r,p,q):
        self.uid = uid
        self.r=r
        self.p=p
        self.q=q
        
class machine:
    def __init__(self,*argv):
        self.procs = list(argv)
        
    def run(self):
        current_time = 0
        max_end = 0
        for proc in procs:
            current_time = max(proc.r,current_time)
#            print(proc.uid,'at',current_time)
            proc.start_time = current_time
            current_time = current_time+proc.p
            max_end = max(max_end,current_time+proc.q)
        return max_end
            
        
from random import random
from itertools import permutations
import numpy as np

maxN = 7
Ns = list(range(1,maxN+1))

avg_sortr = np.zeros(maxN)
avg_przeg = np.zeros(maxN)

num_of_iterations = 50

for t in range(num_of_iterations):
    sortr = []
    przeg = []
    
    for N in Ns: 
    #    N = 5
        max_t = 9
        procs = []
        
        for i in range(N):
            procs.append(proc(i,
                              int(random()*max_t)+1,
                              int(random()*max_t)+1,
                              int(random()*max_t)+1))
            
        
        sortr_time = machine(*sorted(procs,key=lambda x:x.r)).run()
        sortr.append(sortr_time)
        
        min_time = (N+2)*max_t+1
        for perm in permutations(procs):
            procs = list(perm)
            min_time = min(min_time,machine(*procs).run())
            
        przeg.append(min_time)
    
    avg_sortr = np.array(avg_sortr) + np.array(sortr)
    avg_przeg = np.array(avg_przeg) + np.array(przeg)
    
    
import matplotlib.pyplot as plt
plt.plot(Ns,avg_sortr/num_of_iterations,Ns,avg_przeg/num_of_iterations)

