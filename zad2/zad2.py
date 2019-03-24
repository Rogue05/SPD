# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 12:33:07 2019

@author: Wojtek
"""
from Process import *
from copy import deepcopy

def insertions(elem,base_list):
    for i in range(len(base_list)+1):
        yield [*base_list[0:i],elem,*base_list[i:]]
        
def removals(elem,base_list):
    for i in range(len(base_list)):
        yield [*base_list[0:i],*base_list[i+1:]]

def add_proc_to_time(t,nthproc):
    if t is None:
        t = [0]*len(nthproc.p)
#    else:
#        t = deepcopy(t)
    nthproc.start = []
    for machine_nr in range(len(nthproc.p)):
        if machine_nr == 0:
            nthproc.start = [t[machine_nr],]
            t[machine_nr] = t[machine_nr]+nthproc.p[machine_nr]
        else:
            nthproc.start.append(max(t[machine_nr],t[machine_nr-1]))
            t[machine_nr] = max(t[machine_nr],t[machine_nr-1])+nthproc.p[machine_nr]
    return t

#def get_pipe_cost(N,return_pipe=False):
#    t = [0]*len(N[0].p)
#    
#    for nthproc in N:
#        t = add_proc_to_time(t,nthproc)
##        nthproc.start = []
##        for machine_nr in range(len(nthproc.p)):
##            if machine_nr == 0:
##                nthproc.start = [t[machine_nr],]
##                t[machine_nr] = t[machine_nr]+nthproc.p[machine_nr]
##            else:
##                nthproc.start.append(max(t[machine_nr],t[machine_nr-1]))
##                t[machine_nr] = max(t[machine_nr],t[machine_nr-1])+nthproc.p[machine_nr]
##    if return_pipe:
##        return N
#    return max(t)

def pipe_to_str(pipe):
    return ' '.join([str(proc.uid) for proc in pipe])

def my_min(elem,new_order):
    t = add_proc_to_time(None,elem)
    cached_t = [0]*len(t)
    best_i = 0
    for i in range(len(new_order)):
        add_proc_to_time(t,new_order[i])
    best_t=max(t)        
    for i in range(len(new_order)):
        add_proc_to_time(cached_t,new_order[i])
        tmp_t = deepcopy(cached_t)
        tmp_t = add_proc_to_time(tmp_t,elem)
        for j in range(i+1,len(new_order)):
            add_proc_to_time(tmp_t,new_order[j])
        max_tmp_t = max(tmp_t)
        if max_tmp_t < best_t:
            best_t = max_tmp_t
            best_i = i+1
            
    return [*new_order[0:best_i],elem,*new_order[best_i:]]
    
def NEH(N,boost=True):
    new_order = []
#    get_pipe_cost.clear_cache()
    for elem in sorted(N,key=lambda x:1/sum(x.p)):
        if not boost:
#            print('not boosted')
            new_order = min(insertions(elem,new_order),key=lambda x:get_pipe_cost(x))
        else:
#            print('boosted')
            new_order = my_min(elem,new_order)
        
    return new_order
    
with open('neh.data.txt','r') as file:
    lines = file.readlines()
    
class Dataset:
    pass

datasets = [];i=0;pid=0
readdata = False
ignorenext = False
for line in lines:
#    if i < 10:
#        print(len(line.split('.'))==2)
    if len(line.split('.')) == 2:
        datasets.append(Dataset())
        datasets[-1].uid = i
        datasets[-1].data = []
        i=i+1
        pid = 1
        readdata = True
        ignorenext = True
    if len(line.split(':')) == 2 and line.split(':')[0]=='neh':
        readdata = False
    if len(line.split(' ')) == 1 and not readdata and line != 'neh:\n' and line != '\n':
        datasets[-1].cost = int(line.split(' ')[0])
    if len(line.split(' ')) > 1 and readdata:
        if ignorenext:
            ignorenext = False
            continue
        margv = []
        for p in line.split(' '):
            margv.append(int(p))
        datasets[-1].data.append(processPipe(pid,*margv))
        pid = pid + 1
        
i = 0;ok=0
out = []

import time

for dataset in datasets:
    i = i + 1
    if i > 100:
        continue
#    print('call')
    out.append(Dataset())
    start = time.time()
    order = NEH(dataset.data,boost=False)
    out[-1].time= time.time() - start
#    c = get_pipe_cost.cache
#    order = []
    if get_pipe_cost(order) == dataset.cost:
        ok = ok+1
    out[-1].uid = i
    out[-1].mycost = get_pipe_cost(order)
    out[-1].datacost = dataset.cost
    out[-1].order = ' '.join([str(proc.uid) for proc in order])
    print(i,
          out[-1].time,
          get_pipe_cost(order),
          dataset.cost,
          '{:.2f}%'.format((out[-1].mycost-out[-1].datacost)*100/out[-1].datacost),
#          [proc.uid for proc in order],
          )
    
#    if i==10:
#        break
print('ok',ok)
with open('normal.txt','w') as file:
    for o in out:
        file.write(
                str(o.uid)+';'+
                str(o.time)+';'+
                str(o.mycost)+';'+
                str(o.datacost)+';'+
                o.order+'\n')
print('saved')

#end = time.time()
#print('time: ',end-start)
# noboost nocache 893.081104516983
# noboost cache 332.2397389411926
# boost 336.8780333995819
#79 [11, 85, 91, 102, 97, 98, 96, 18, 84, 34, 47, 32, 12, 82, 74, 99, 81, 100, 52, 101, 73, 53, 42, 55, 56, 103, 30, 36, 87, 54, 51, 49, 50, 88, 79, 58, 62, 33, 38, 27, 90, 77, 75, 72, 41, 44, 40, 13, 5, 66, 43, 37, 69, 22, 61, 59, 23, 20, 83, 19, 21, 8, 25, 60, 94, 0, 14, 9, 2, 15, 3, 28, 17, 4, 6, 93, 29, 35, 31, 26, 7, 10, 16, 45, 67, 39, 57, 89, 63, 70, 68, 86, 95, 71, 48, 64, 92, 46, 24, 1, 76, 80, 65, 78]