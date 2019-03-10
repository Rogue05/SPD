# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 20:49:22 2019

@author: Wojtek
"""
from Process import *
from copy import deepcopy

def Schrage(N):
    Cmax=0
    sig=[]
    Ng=[]
    Nn=deepcopy(N)
    t=min(Nn,key=lambda x:x.r).r
    while Ng != [] or Nn != []:
        while Nn != [] and min(Nn,key=lambda x:x.r).r <= t:
            j = min(Nn,key=lambda x:x.r)
            Ng.append(j)
            Nn.remove(j)
        if Ng == []:
            t = min(Nn,key=lambda x:x.r).r
        else:
            j = max(Ng,key=lambda x:x.q)
            Ng.remove(j)
            sig.append(j)
            t=t+j.p
            Cmax = max(t+j.q,Cmax)
    return sig,Cmax

def SchragePmtn(N):
    sig=[]
    Ng=[]
    Nn=deepcopy(N)
    Cmax = 0
    t=0
    l=Nn[0] # zerowe zadanie, a nie zero
#    l.q=1000000000
    while Ng != [] or Nn != []:
        while Nn != [] and min(Nn,key=lambda x:x.r).r <= t:
            j = min(Nn,key=lambda x:x.r)
#            print('Moving',j.uid)
            Ng.append(j)
            Nn.remove(j)
            if j.q > l.q: #przerywam ostatni l, zaczynam j
#                l.p = t-j.r
#                t = j.r
                
                nl = deepcopy(l)
                nl.p=t-j.r
#                print(l.uid,'vs',j.uid,'-',t-j.r,l.p,j.r)
                t=j.r
                if nl.p > 0:
                    l.q=0
                    nl.r=0
                    l.p=l.p-nl.p # zeby ladnie wygladalo
                    Ng.append(nl) # wtf bez tego dziala dla 100 i 200 
                    
            
        if Ng == []:
            t = min(Nn,key=lambda x:x.r).r
        else:
            j = max(Ng,key=lambda x:x.q)
            Ng.remove(j)
            l=j
            j.start=t
            sig.append(j)
            t=t+j.p
            Cmax = max(Cmax,t+j.q)
    return sig,Cmax

#def Calier(N):
#    U = Schrage(N)
#    UB = 1000000000
#    LB = 0
#    if U < UB:
#        UB = get_cost(U)
#        minpi = U


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
    datasets = [[]]
    for filename in ['in50.txt','in100.txt','in200.txt']:
        procs = []
        print('\nProcessing',filename)
        with open('dane_testowe/'+filename,'r') as file:
            lines = file.readlines()
            
        uid = 0
        for line in lines[1:]:
            line=line.strip().split()
            procs.append(process(uid,int(line[0]),int(line[1]),int(line[2])))
            uid = uid + 1
        datasets.append(procs)
        datasets[0]=[*datasets[0],*procs]
#    datasets.append([*datasets[3],*datasets[2],*datasets[1]])
#    datasets.append([*datasets[2],*datasets[1],*datasets[3]])
#    datasets.append([*datasets[1],*datasets[2],*datasets[3]])
#    datasets.append([*datasets[3],*datasets[1],*datasets[2]])
#    datasets.append([*datasets[1],*datasets[3],*datasets[2]])
#    datasets.append([*datasets[2],*datasets[3],*datasets[1]])
        
#        N=200
#        max_t=50
#        for i in range(N):
#            procs.append(process(i,
#                              int(random()*max_t)+1,
#                              int(random()*max_t)+1,
#                              int(random()*max_t)+1))
        
    import plotly.plotly as py
    import plotly.figure_factory as ff
    
    for procs in datasets:
        proc_dict = {proc.uid:proc for proc in procs}
        order,order_cost = Schrage(procs)
        pmtno,pmtnc = SchragePmtn(procs)
        
        print('\nlen of data ',len(procs))
        print('Schrage     ',order_cost)
        print('Schrage Pmtn',pmtnc)
        print('diff',order_cost-pmtnc,get_cost(order)-get_cost(pmtno))
        
        df = [dict(
                Task=proc.uid,
                Start=proc.start,
                Finish=proc.start+proc.p) for proc in order]
        fig = ff.create_gantt(df)
        py.iplot(fig, filename='gantt-simple-gantt-chart')
        print(order_cost==get_cost(order),pmtnc==get_cost(pmtno))
        
    
    
    
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
datasets = [[]]
for filename in ['in50.txt','in100.txt','in200.txt']:
    procs = []
    print('\nProcessing',filename)
    with open('dane_testowe/'+filename,'r') as file:
        lines = file.readlines()
        
    uid = 0
    for line in lines[1:]:
        line=line.strip().split()
        procs.append(process(uid,int(line[0]),int(line[1]),int(line[2])))
        uid = uid + 1
    datasets.append(procs)
    datasets[0]=[*datasets[0],*procs]
    
import plotly.plotly as py
import plotly.figure_factory as ff

for procs in datasets:
    proc_dict = {proc.uid:proc for proc in procs}
    order,order_cost = Schrage(procs)
    pmtno,pmtnc = SchragePmtn(procs)
    
    print('\nlen of data ',len(procs))
    print('Schrage     ',order_cost)
    print('Schrage Pmtn',pmtnc)
    print('diff',order_cost-pmtnc,get_cost(order)-get_cost(pmtno))
    
    df = [dict(
            Task=proc.uid,
            Start=proc.start,
            Finish=proc.start+proc.p) for proc in order]
    fig = ff.create_gantt(df)
    py.plot(fig, filename='gantt-simple-gantt-chart')
    print(order_cost==get_cost(order),pmtnc==get_cost(pmtno))
    
    
    
    