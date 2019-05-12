# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 20:59:45 2019

@author: Wojtek
"""


class process:
    def __init__(self,uid,r,p,q):
        self.uid = uid
        self.r=r
        self.p=p
        self.q=q
    
    def __str__(self):
        return ' '.join([
                str(self.uid),
                str(self.r),
                str(self.p),
                str(self.q)
                ])
    
    def __lt__(a,b):
        return a.q<b.q
    def __gt__(a,b):
        return a.q>b.q


def get_cost(N):
    end = 0
    t = 0
    for nthproc in N:
        t = max(t,nthproc.r)+nthproc.p
        end = max(nthproc.q+t,end)
    return end