# -*- coding: utf-8 -*-
"""
Created on Sat Apr  6 13:41:32 2019

@author: Wojtek
"""

from Process import *
from copy import deepcopy
from math import exp
from random import random

def swap_noighbours_move(order):
    norder = deepcopy(order)
    i = int((random()*len(norder))%(len(norder)-1))
    j = i+1
#    print(i)
    norder[i],norder[j] = norder[j],norder[i]
    return norder

def swap_random_move(order):
    norder = deepcopy(order)
    i = int((random()*len(norder))%(len(norder)))
    j = int((random()*len(norder))%(len(norder)))
#    print(i)
    norder[i],norder[j] = norder[j],norder[i]
    return norder

def insert_move(order):
    norder = deepcopy(order)
    i = int((random()*len(norder))%(len(norder)-1))
    j = int((random()*len(norder))%(len(norder)-1))
    elem = norder[i]
    norder.remove(elem)
    norder.insert(j,elem)
    return norder
    

def default_kryt(c1,c2,T):
    if c2<c1:
        return True
    return False #exp((c1-c2)/T)

def wyzarzanie(order,*,
               T=100,
               schemat_chlodzenia=lambda x,i:x*0.99,
               wykonaj_ruch=swap_noighbours_move,
               kryterium_stopu=lambda x:x>1,
               kryterium_ruchu=default_kryt):
    
    best_order = order
    best_cost = get_cost(best_order)
    i = 1
    while kryterium_stopu(T):
        new_order = wykonaj_ruch(order)
        cost = get_cost(new_order)
        if kryterium_ruchu(best_cost,cost,T):
#            print('---',best_cost,cost)
            best_cost = cost
            best_order = new_order
        T=schemat_chlodzenia(T,i)
        i+=1
    return best_order