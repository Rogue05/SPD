# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 21:02:24 2019

@author: Wojtek
"""

from Process import *
from copy import deepcopy
from itertools import permutations
from functools import partial

def sortR(N):
    return sorted(N,key=lambda x:x.r)

def checkAll_uni(cost_func,N):
    min_time = 10000000000
    best_perm = deepcopy(N)
    for perm in permutations(N):
        procs = list(perm)
        new_min_time = cost_func(procs)
        if new_min_time < min_time:
            min_time = new_min_time
            best_perm = procs
    return deepcopy(best_perm),min_time

checkAll = partial(checkAll_uni,get_cost)
checkAllPipes = partial(checkAll_uni,get_pipe_cost)
    
def Johnson2(N):
    upper = []
    lower = []
    N = deepcopy(N)
    nN = []
    while len(N) > 0:
        min_proc0 = min(N,key=lambda x:x.p[0])
        min_proc1 = min(N,key=lambda x:x.p[1])
        if min_proc1.p[1] < min_proc0.p[0]:
            N.remove(min_proc1)
            upper.append(min_proc1)
        else:
            N.remove(min_proc0)
            lower.append(min_proc0)
    upper.reverse()
    nN = [*lower,*upper]
    return nN

def Johnson3(N):
    new_pipe = [processPipe(proc.uid,proc.p[0]+proc.p[1],proc.p[1]+proc.p[2]) 
                for proc in N]
    proc_dict = {proc.uid:proc for proc in N}
    
    order = Johnson2(new_pipe)
    new_order = [proc_dict[proc.uid] for proc in order]
    return get_pipe_cost(new_order,True)

if __name__ == '__main__':
    
    from sys import argv
    import plotly.offline as py
    import plotly.figure_factory as ff

    py.init_notebook_mode(connected=True)
    
    filename = 'ta000.txt'
    
    if len(argv) == 1:
        argv.append(filename)
#    if len(argv) >= 2:
#        filename = argv[1]
    for filename in argv[1:]:
            
        with open(filename,'r') as file:
            lines = file.readlines()
            
        pipe = []
        num_of_lines = int(lines[0].strip().split('   ')[0])
        num_of_machines = int(lines[0].strip().split('   ')[1])
        for i in range(1,num_of_lines+1):
    #    for line in lines:
            data = lines[i].strip().split('   ')
            for j in range(num_of_machines):
                data[j]=int(data[j])
            pipe.append(processPipe(i,*data))
        
        if num_of_machines == 3:
            jorder = Johnson3(pipe)
            print('Johnson3',get_pipe_cost(jorder))
        elif num_of_machines == 2:
            jorder = Johnson2(pipe)
            print('Johnson2',get_pipe_cost(jorder))
        jorder = get_pipe_cost(jorder,True)
        print('j',[(proc.uid,proc.start) for proc in jorder],'\n')   
        
        df = []
        for machine in range(len(jorder[0].start)):
            for proc in jorder:
                df.append(dict(
                        Task=str(machine),
                        Start=str(proc.start[machine]+1000)+'-01-01',
                        Finish=str(proc.start[machine]+proc.p[machine]+1000)+'-01-01',
                        Resource=str(proc.uid)))
        
        fig = ff.create_gantt(df,index_col='Resource',group_tasks=True,show_colorbar=True)
        py.plot(fig)

        aorder = checkAllPipes(pipe)[0]
        print('przeglad zupelny',get_pipe_cost(aorder))
        print('a',[(proc.uid,proc.start) for proc in aorder],'\n')
        
#    pipe = [
#    processPipe('a',3.2,4.2),
#    processPipe('b',4.7,1.5),
#    processPipe('c',2.2,5.0),
#    processPipe('d',5.8,4.0),
#    processPipe('e',3.1,2.8)
#    ]
#    order = Johnson2(pipe)
#    print('Johnson2',get_pipe_cost(order))
#    print('all check',checkAllPipes(order)[1])
#    
#    print([proc.uid for proc in order],'\n')
#    pipe = [
#    processPipe(1,5,5,3),
#    processPipe(2,4,5,2),
#    processPipe(3,4,4,5),
#    processPipe(4,3,5,7)
#    ]
#    order = Johnson3(pipe)
#    print('Johnson3',get_pipe_cost(order))
#    print('all check',checkAllPipes(order)[1])
#    print([proc.uid for proc in order],'\n')
    