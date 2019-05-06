# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 21:02:24 2019

@author: Wojtek
"""

from Process import *
from copy import deepcopy

def sortR(N):
    return sorted(N,key=lambda x:x.r)

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