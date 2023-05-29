#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  3 17:04:49 2023

######################################################
#                                                    #
# Valores máximos de C_B experimentales y simulados  #
# para cada caso                                     #
#                                                    #      
######################################################
    
@author: fneme
"""

#%% CARGA DE LIBRERIAS
# = = = = = = = = = = =

import pandas as pd


#%% DATOS EXPERIMENTALES 
# = = = = = = = = = = =

datos_exp = pd.read_csv('../../ImportarDatos/DatosExp/20221104/LNPa22_GSuSIN.csv', decimal = '.')

# Encontrar el índice de la fila con el valor máximo de C_B

max_index_exp = datos_exp['C_B'].idxmax()

# Extraer el valor de C_B y t  correspondiente al índice anterior

C_B_max_exp = datos_exp.loc[max_index_exp, 'C_B']
t_C_B_max_exp = datos_exp.loc[max_index_exp, 't']

#%% DATOS SIMULADOS 
# = = = = = = = = =

datos_sim = pd.read_csv('../04_Salidas/LNPa22-Estimaciones/T02_Modelo_BNSE_kd1e-5/CAS_20230503_1548_CAS_LNPa22_GSuSIN/4A_ResultadosModelo.csv', decimal = '.')

# Encontrar el índice de la fila con el valor máximo de C_B

max_index_sim = datos_sim['C_B'].idxmax()

# Extraer el valor de C_B y t  correspondiente al índice anterior

C_B_max_sim = datos_sim.loc[max_index_sim, 'C_B']
t_C_B_max_sim = datos_sim.loc[max_index_sim, '[t]']/24

