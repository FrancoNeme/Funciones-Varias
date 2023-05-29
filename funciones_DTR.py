#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 20:05:16 2023

#############################
#                           #                                                 
# MODULO DE FUNCIONES DTR   #
#                           #
#############################

@author: Franco Neme
"""

#%% CARGA DE LIBRERIAS
# = = = = = = = = = = 

import numpy as np
from scipy.integrate import simpson


#%% FUNCIONES
# = = = = = =

# FUNCION E_t
# -----------

def Func_E_t(C_tr,t):
    
    E_t = C_tr/simpson(C_tr,t)
    
    return E_t



# FUNCION F_t
# -----------

def Func_F_t(E_t,t):
    
    F_t = np.empty(len(E_t))
    
    for i in range(1,len(E_t)+1):
        
        F_t[i-1] = simpson(E_t[:i],t[:i])
    
    return F_t



# FUNCION t_m
# -----------

def Func_t_m(E_t,t):
    
    t_m = simpson(t * E_t,t)
    
    return t_m


    
# FUNCION s_2
# -----------    

def Func_s_2(t,t_m,E_t):
    
    s_2 = simpson( ((t - t_m)**2 )* E_t, t)
    
    return s_2


# FUNCION E(Z)
# ------------

def Func_E_Z(t,t_m):
    
    Z = t/t_m
    
    E_Z = np.exp(-Z)
    
    return E_Z
