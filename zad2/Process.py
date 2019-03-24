# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 20:59:45 2019

@author: Wojtek
"""


class process:
    def __init__(self,uid,r=0,p=0,q=0):
        self.uid = uid
        self.r=r
        self.p=p
        self.q=q
    def __str__(self):
        return str(self.uid)+' '+str(self.r)+' '+str(self.p)+' '+str(self.q)
        
class processPipe:
    def __init__(self,uid,*argv):
        self.uid = uid
        self.p = argv
    def __str__(self):
        return str(self.uid)+' '+str(self.p)
         
def pipe_hash(pipe):
    return ' '.join([str(proc) for proc in pipe])    

from copy import deepcopy

#class get_pipe_cost_class:
#    def __init__(self):
#        self.cache = {}
#        
#    def clear_cache(self):
#        self.cache = {}
##        print('Cleared cache')
#    
#    def __call__(self,N,return_pipe=False,t = [], use_cache = False):
#        if len(N) == 0:
#            return 0 
#        t = [0]*len(N[0].p)
#        
#        if not use_cache:
#            self.cache = {}
#        
#        ind = []
#        
#        for nthproc in N:
#            nthproc.start = []
#            ind.append(nthproc.uid)
##            cached_t = None
#            cached_t = self.cache.get(pipe_hash(ind))
#            if cached_t is None:
#                for machine_nr in range(len(nthproc.p)):
#                    if machine_nr == 0:
#                        nthproc.start = [t[machine_nr],]
#                        t[machine_nr] = t[machine_nr]+nthproc.p[machine_nr]
#                    else:
#                        nthproc.start.append(max(t[machine_nr],t[machine_nr-1]))
#                        t[machine_nr] = max(t[machine_nr],t[machine_nr-1])+nthproc.p[machine_nr]
#                if use_cache:
#                    self.cache[pipe_hash(ind)] = deepcopy(t)
#            else:
#                t = deepcopy(cached_t)
#        if return_pipe:
#            return N
#        return max(t)
#    
#get_pipe_cost = get_pipe_cost_class()

def get_pipe_cost(N,return_pipe=False):
    t = []
    for _ in range(100):
        t.append(0)
    for nthproc in N:
        nthproc.start = []
        for machine_nr in range(len(nthproc.p)):
            if machine_nr == 0:
                nthproc.start = [t[machine_nr],]
                t[machine_nr] = t[machine_nr]+nthproc.p[machine_nr]
            else:
                nthproc.start.append(max(t[machine_nr],t[machine_nr-1]))
                t[machine_nr] = max(t[machine_nr],t[machine_nr-1])+nthproc.p[machine_nr]
    if return_pipe:
        return N
    return max(t)
        

def get_cost(N):
    end = 0
    t = 0
    for nthproc in N:
        nthproc.start = t
        t = max(t,nthproc.r)+nthproc.p
        end = max(nthproc.q+t,end)
    return end


    