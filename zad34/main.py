# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 21:00:54 2019

@author: Wojtek
"""

from Schrage import *
from zad1 import *

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
    
for procs in datasets:
    proc_dict = {proc.uid:proc for proc in procs}
    order,order_cost = Schrage(procs)
    pmtno,pmtnc = SchragePmtn(procs)
    
    print('\nlen of data  ',len(procs))
    print('Schrage      ',order_cost)
    print('Schrage Pmtn ',pmtnc)
    print('sortR        ',get_cost(sortR(procs)))
    print('diff',order_cost-pmtnc,get_cost(order)-get_cost(pmtno))
    assert order_cost==get_cost(order)
    assert pmtnc==get_cost(pmtno)
        
    