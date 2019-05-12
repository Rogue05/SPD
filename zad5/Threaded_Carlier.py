# -*- coding: utf-8 -*-
"""
Created on Fri May 10 16:43:49 2019

@author: Wojtek
"""

# -*- coding: utf-8 -*-
"""
Created on Fri May 10 13:17:58 2019

@author: Wojtek
"""

from Process import *
from Schrage import *

from copy import copy

def get_abc(order):
    b = max(order,key=lambda x:x.end+x.q)
    c = None
    a = None
    for i in range(order.index(b),0,-1):
#        print(b.uid)
        if not order[i-1].end == order[i].start:
            break
        a=order[i-1]
        if a.q < b.q and c is None:
            c = a
    return a,b,c
    
def h_fun(K):
    rK = min(K,key=lambda x:x.r).r
    qK = min(K,key=lambda x:x.q).q
#    pK = K[-1].end-K[0].start
    pK = sum([k.p for k in K])
    return rK+pK+qK

def print_order(order, soft=False):
    print('-',[p.uid for p in order], get_cost(order))
    if not soft:
        order=copy(order)
        order.sort(key=lambda x:x.uid)
        print([p.r for p in order])
        print([p.q for p in order])
        print([p.p for p in order])

r = [10,13,11,20,30,0,30]
p = [5,6,7,4,3,6,2]
q = [7,26,24,21,8,17,0]

procs = []

for i in range(len(r)):
    procs.append(process(i+1,r[i],p[i],q[i]))
del r;del p;del q


import threading

def Carlier(order):
    class dummyc:
        def __init__(self):
            self.optimum = []
            self.stack = []
            self.UB = 10000000
            self.lock = threading.Lock()
            self.threads = []
            self.threaded_depth = 0
        def check_sol(self, order, U):
            with self.lock:
                if U < dummy.UB:
                    self.optimum = copy(order)
                    self.UB=U
            
    def InnerCarlier(order,dummy):
        global to_check
        order, U = Schrage(order)
#        if U < dummy.UB:
#            dummy.optimum = copy(order)
#            dummy.UB=U
        dummy.check_sol(order,U)
        
        a,b,c = get_abc(order)
        if c is None:
            return
        
        K = order[order.index(c)+1:order.index(b)+1]
        
        rK = min(K,key=lambda x:x.r).r
        qK = min(K,key=lambda x:x.q).q
        pK = sum([k.p for k in K])
        
        prev_r = c.r
        c.r = max(c.r,rK+pK)
        garbage, LB = SchragePmtn(order)
        LB = max(LB,rK+pK+qK,h_fun([*K,c]))
        if LB < dummy.UB:
            if len(dummy.stack) < dummy.threaded_depth:
                dummy.stack.append('Q')
                InnerCarlier(order,dummy)
                dummy.stack.pop()
            elif len(dummy.stack) == dummy.threaded_depth:
#                print('adding')
                dummy.threads.append(threading.Thread(
                        target=InnerCarlier,
                        args=(deepcopy(order),dummy)
                        ))
            else:
                InnerCarlier(order,dummy)
        c.r = prev_r
    
        prev_q = c.q
        c.q = max(c.q,qK+pK)
        garbage, LB = SchragePmtn(order)
        LB = max(LB,h_fun(K),h_fun([*K,c]))
        if LB < dummy.UB:
            if len(dummy.stack) < dummy.threaded_depth:
                dummy.stack.append('Q')
                InnerCarlier(order,dummy)
                dummy.stack.pop()
            elif len(dummy.stack) == dummy.threaded_depth:
                print('adding')
                dummy.threads.append(threading.Thread(
                        target=InnerCarlier,
                        args=(deepcopy(order),dummy)
                        ))
            else:
                InnerCarlier(order,dummy)
        c.q = prev_r
    dummy = dummyc()
    dummy.stack=[0]*10 # enabling/disabling threading
    InnerCarlier(order,dummy)
    print('Running in',len(dummy.threads),'threads')
    dummy.stack=[0]*10
    
    for t in dummy.threads:
        t.start()
    for t in dummy.threads:
        t.join()
    dummy.threads = []
    return dummy.optimum, dummy.UB

optimum, UB = Carlier(procs)
fin = [p.uid for p in optimum]
print(fin,UB)

def superp(arg):
    out = []
    for a in arg:
        out = [*out,*a]
    return out

datasets = []
for filename in [
        'in50.txt',
        'in100.txt',
        'in200.txt',
        ]:
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
#datasets.append(deepcopy(superp(datasets)))

import time
out = []
for procs in datasets:
    print(len(procs))
    
    start = time.time()
    sch_o,sch_c = Schrage(procs)
    sch_t = time.time()-start
    
    start = time.time()
    optimum, UB = Carlier(procs)
    car_t = time.time()-start
    print('\nlen of data ',len(procs))
    print('Carlier',
#          [p.uid for p in optimum],
          UB,
          car_t)
    print('Schrage',
#          [p.uid for p in sch_o],
          sch_c,
          sch_t)
    
        
    

"""
MUD


"""