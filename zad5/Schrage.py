# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 20:49:22 2019

@author: Wojtek
"""
from Process import *
from copy import deepcopy,copy
from bisect import insort
from wyzazanie import *

def Schrage(N):
    Cmax=0
    sig=[]
    sNg=[]
    Nn=deepcopy(N)
    Nn.sort(key=lambda x:x.r)
    t=Nn[0].r
    while sNg != [] or Nn != []:
        while Nn != [] and Nn[0].r <= t:
            j = Nn[0]
#            Ng.append(j)
            insort(sNg,j)
            Nn.pop(0)
        if sNg == []:
            t = Nn[0].r
        else:
            j = sNg.pop()
#            j = max(Ng,key=lambda x:x.q)
#            Ng.remove(j)
            sig.append(j)
            j.start=t
            t=t+j.p
            j.end=t
            Cmax = max(t+j.q,Cmax)
    return sig,Cmax

def SchragePmtn(N):
    sig=[]
    sNg=[]
    Nn=deepcopy(N)
    Nn.sort(key=lambda x:x.r)
    
    Cmax = 0
    t=0
    l=Nn[0]
    while sNg != [] or Nn != []:
        while Nn != [] and Nn[0].r <= t:
            j = Nn[0]
#            Ng.append(j)
            insort(sNg,j)
            Nn.pop(0)
            if j.q > l.q: 
                nl = deepcopy(l)
                nl.p=t-j.r
                t=j.r
                if nl.p > 0:
                    l.q=0
                    nl.r=0
                    l.p=l.p-nl.p
#                    Ng.append(nl)
                    insort(sNg,nl)
                    
        if sNg == []:
            t = Nn[0].r
        else:
            j = sNg.pop()
#            Ng.remove(j)
            l=j
            j.start=t
            sig.append(j)
            t=t+j.p
            j.end=t
            Cmax = max(Cmax,t+j.q)
    return sig,Cmax

if __name__=='__main__':    
    
    from random import random
    # dane prof Smutnickiego
    #r=[10,13,11,20,30,0, 30];
    #p=[5, 6, 7, 4, 3, 6, 2];
    #q=[7, 26,24,21,8, 17,0];
    #procs = []
    #for i in range(len(r)):
    #    procs.append(process(i+1,r[i],p[i],q[i]))
    #
    #order,order_cost = Schrage(procs)
    #pmtno,pmtnc = SchragePmtn(procs)
    #print('Schrage     ',order_cost)
    #print('Schrage Pmtn',pmtnc)
    #del p;del r;del q;del i;del procs;
    
    #dane przykladowe
#    datasets = [[]]
    datasets = []
    for filename in [
            'in50.txt','in100.txt','in200.txt',
#            '10000.txt'
            ]:
        procs = []
        print('\nProcessing',filename)
        with open('dane_testowe/'+filename,'r') as file:
            lines = file.readlines()
            
        uid = 0
        for line in lines[1:]:
            line=line.strip().split()
            procs.append(process(uid,int(line[0]),int(line[1]),int(line[2])))
#            print(uid)
            uid = uid + 1
#            if uid>1000:
#                break
#            if uid%100==0:
#                datasets.append(copy(procs))
        datasets.append(procs)
    import time
    out = []
    for procs in datasets:
        print(len(procs))
        proc_dict = {proc.uid:proc for proc in procs}
        start = time.time()
        order,order_cost = Schrage(deepcopy(procs))
        sch_t = time.time()-start
        start = time.time()
        pmtno,pmtnc = SchragePmtn(deepcopy(procs))
        sch_pmtn_t = time.time()-start
#        start = time.time()
#        test_c=wyzarzanie(deepcopy(order))
#        w_sch_t = time.time()-start
        out.append((sch_t/len(order),
                    sch_pmtn_t/len(order)
#                    0
                    ))
        print('\nlen of data ',len(procs))
        print('Schrage     ',order_cost, sch_t)
        print('Schrage Pmtn',pmtnc, sch_pmtn_t)
#        print('Schrage + wyzarzanie',get_cost(test_c),w_sch_t)
        print('diff',order_cost-pmtnc,get_cost(order)-get_cost(pmtno))
        print(order_cost==get_cost(order),pmtnc==get_cost(pmtno))
#    import matplotlib.pyplot as plt
#    plt.plot([o[0] for o in out])
#    plt.plot([o[1] for o in out])
    #
        
    