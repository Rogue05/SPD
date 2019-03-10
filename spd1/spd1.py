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
max_t = 9

def get_cost(N):
    end = 0
    t = 0
    for nthproc in N:
        t = max(t,nthproc.r)+nthproc.p
        end = max(nthproc.q+t,end)
    return end

def sortR(N):
    return sorted(N,key=lambda x:x.r)

from copy import deepcopy

def checkAll(N):
    min_time = 10000000000
    best_perm = N
    for perm in permutations(N):
        procs = list(perm)
        new_min_time = get_cost(procs)
        if new_min_time < min_time:
            min_time = new_min_time
            best_perm = procs
    return deepcopy(best_perm)
        

for t in range(num_of_iterations):
#    print('Iter',t)
    sortr = []
    przeg = []
    
    for N in Ns:
        procs = []
        
        for i in range(N):
            procs.append(proc(i,
                              int(random()*max_t)+1,
                              int(random()*max_t)+1,
                              int(random()*max_t)+1))
            
        
        sortr_time = get_cost(procs)
        sortr.append(sortr_time)
        
#        min_time = (N+2)*max_t+1
#        for perm in permutations(procs):
#            procs = list(perm)
#            min_time = min(min_time,machine(*procs).run())
        min_time = get_cost(checkAll(procs))
        przeg.append(min_time)
    
    avg_sortr = np.array(avg_sortr) + np.array(sortr)
    avg_przeg = np.array(avg_przeg) + np.array(przeg)
    
    
import matplotlib.pyplot as plt

plt.plot(Ns,avg_sortr/num_of_iterations,Ns,avg_przeg/num_of_iterations)
print((avg_sortr-avg_przeg)/np.array(Ns))

