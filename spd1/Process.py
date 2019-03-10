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
            
def get_pipe_cost(N,return_pipe=False):
    t = [0,0,0]
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


    