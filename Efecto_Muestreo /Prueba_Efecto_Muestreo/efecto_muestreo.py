#import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
import seaborn as sns



#%% CARGA DE DATOS Y CSV DE SALIDA

## Datos crudos ----

datos = []; datos = pd.DataFrame(datos)

ls = os.listdir('../Run03_re-ejecuciones_todo_nuevosDatos')
ls.sort()

for i in ls:
    directorio = '../Run03_re-ejecuciones_todo_nuevosDatos/' + i + '/0_Resutls_Abstract.csv'
    datos = datos.append(pd.read_csv(directorio))

indices = list(range(0,len(ls))); datos.index = indices # esto de indexar es necesario porque despues cuando appendeo
                                                        # "dt" y "error" necesito que los indices de los tres df sean
                                                        # los mismos
del datos['Unnamed: 0']


## Reorganizar csv salida ----

casos = pd.DataFrame.copy((datos['Caso']))

Δt = []
error = []

for i in casos:
    j = i[2:4]
    k = i[5:]
    Δt.append(j)
    error.append(k)

Δt = pd.DataFrame(Δt);Δt.columns=['Δt']
error = pd.DataFrame(error);error.columns=['error']

datos.insert(1,"Δt",Δt,True);datos.insert(2,"error",error,True)


## Exporto csv ----

try:
    os.mkdir('../Salidas') # Creo directorio para las salidas del script
except:
    pass # Si ya existe el directorio (por ejemplo cuando corro el script por segunda vez).
         # Lo hago para que no me salte un "error" (no modifica nada, solo no me gusta que
         # salte el "mensaje de error" en la consola)

datos.to_csv('../Salidas/datos.csv',index=False)

#%% GRAFICOS PARMS

## Creacion del directorio y armado de objetos necesarios ----

try:
    os.mkdir('../Salidas/Parms')
except:
    pass

cabeceras = list(datos.columns.values.tolist())
parms = list.copy(cabeceras[3:9])
unidades_parms = ("[1/h]","[gN/L]","[gN/gB]","[gE/(gB.h)]","[gS/L]","[gS/gE]")

## Preseteo de grafica ----

parametros_context_poster = dict(sns.plotting_context("poster")) # Referencia util para crear el dicionario que conformara el context personalizado
sns.set_style('ticks')
plt.rcParams['figure.figsize'] = 18,16

## Bucle ----

for i in parms:
    
    j = unidades_parms[parms.index(i)]
    
    with plt.style.context({'axes.linewidth': 2.5,
                            'grid.linewidth': 2,
                            'lines.linewidth': 3.0,
                            'lines.markersize': 12,
                            'patch.linewidth': 2,
                            'xtick.major.width': 2.5,
                            'ytick.major.width': 2.5,
                            'xtick.minor.width': 2,
                            'ytick.minor.width': 2,
                            'xtick.major.size': 12,
                            'ytick.major.size': 12,
                            'xtick.minor.size': 8,
                            'ytick.minor.size': 8,
                            'font.size': 50,
                            'axes.labelsize': 24,
                            'axes.titlesize': 24,
                            'xtick.labelsize': 50,
                            'ytick.labelsize': 50,
                            'legend.fontsize': 45,
                            'legend.title_fontsize': 50}):
        
        fig = sns.scatterplot(x="Δt",
                              y=i,
                              hue="error",
                              style="error",
                              edgecolor='b',
                              s = 850,
                              #linewidth=2,
                              #linestyle='--',
                              data=datos)
    
        plt.grid()                           
        plt.legend(bbox_to_anchor=(1.02, 0.77), title = "E [%]", markerscale=2.,loc='upper left')
        fig.set_xlabel( "Δt [h]", weight='bold', size = 50)
        fig.set_ylabel("%s %s" %(i,j), weight='bold', size = 50)
        fig.set_title( "%s %s" %(i,j), weight='bold', size = 50)
    
    figure = plt.gcf()    
    figure.savefig('../Salidas/Parms/%s.png'%i, dpi = 100, bbox_inches='tight')
    fig.figure.clf()



#%% GRAFICOS npRSMD

## Creacion del directorio y armado de objetos necesarios ----

try:
    os.mkdir('../Salidas/npRSMD')
except:
    pass

npRSMD = list.copy(cabeceras[14:18])


## Bucle ----

for i in npRSMD:
    
    
    with plt.style.context({'axes.linewidth': 2.5,
                            'grid.linewidth': 2,
                            'lines.linewidth': 3.0,
                            'lines.markersize': 12,
                            'patch.linewidth': 2,
                            'xtick.major.width': 2.5,
                            'ytick.major.width': 2.5,
                            'xtick.minor.width': 2,
                            'ytick.minor.width': 2,
                            'xtick.major.size': 12,
                            'ytick.major.size': 12,
                            'xtick.minor.size': 8,
                            'ytick.minor.size': 8,
                            'font.size': 50,
                            'axes.labelsize': 24,
                            'axes.titlesize': 24,
                            'xtick.labelsize': 50,
                            'ytick.labelsize': 50,
                            'legend.fontsize': 45,
                            'legend.title_fontsize': 50}):
        
        fig = sns.scatterplot(x="Δt",
                              y=i,
                              hue="error",
                              style="error",
                              edgecolor='b',
                              s = 850,
                              #linewidth=2,
                              #linestyle='--',
                              data=datos)
    
        plt.grid()                           
        plt.legend(bbox_to_anchor=(1.02, 0.77), title = "E [%]", markerscale=2.,loc='upper left')
        fig.set_xlabel( "Δt [h]", weight='bold', size = 50)
        fig.set_ylabel("%s"%i, weight='bold', size = 50)
        fig.set_title( "%s"%i, weight='bold', size = 50)
    
    figure = plt.gcf()    
    figure.savefig('../Salidas/npRSMD/%s.png'%i, dpi = 100, bbox_inches='tight')
    fig.figure.clf()




#%% GRAFICOS DESVIO 

## Creacion del directorio y armado de objetos necesarios ----

try:
    os.mkdir('../Salidas/Desvios')
except:
    pass

mu_mx_orig = 0.119863702 #h^-1
k_dE_orig = 0.000671350 #dm3/(gE.h)
K_N_orig = 0.008826471 # gN/dm3
Y_BN_orig = 30.476929879 #gB/gN
Y_NB_orig = 1/Y_BN_orig
bet_mx_orig = 0.590550575 #gE/(gB.h)
K_S_orig = 10.277941533 #gS/dm3
Y_ES_orig = 0.549910358 #gE/gS
Y_SE_orig = 1/Y_ES_orig


desv_mu_mx = 100*abs((pd.DataFrame.copy(datos["mu_mx"]))/mu_mx_orig - 1)
desv_mu_mx = pd.DataFrame(desv_mu_mx);desv_mu_mx.columns=['desv_mu_mx']

desv_K_N = 100*abs((pd.DataFrame.copy(datos["K_N"]))/K_N_orig - 1)
desv_K_N = pd.DataFrame(desv_K_N);desv_K_N.columns=['desv_K_N']

desv_Y_NB = 100*abs((pd.DataFrame.copy(datos["Y_NB"]))/Y_NB_orig - 1)
desv_Y_NB = pd.DataFrame(desv_Y_NB);desv_Y_NB.columns=['desv_Y_NB']

desv_bet_mx = 100*abs((pd.DataFrame.copy(datos["bet_mx"]))/bet_mx_orig - 1)
desv_bet_mx = pd.DataFrame(desv_bet_mx);desv_bet_mx.columns=['desv_bet_mx']

desv_K_S = 100*abs((pd.DataFrame.copy(datos["K_S"]))/K_S_orig - 1)
desv_K_S = pd.DataFrame(desv_K_S);desv_K_S.columns=['desv_K_S']

desv_Y_SE = 100*abs((pd.DataFrame.copy(datos["Y_SE"]))/Y_SE_orig - 1)
desv_Y_SE = pd.DataFrame(desv_Y_SE);desv_Y_SE.columns=['desv_Y_SE']



desvios = pd.DataFrame.copy(Δt)
desvios.insert(1,"error",error,True);desvios.insert(2,"desv_mu_mx",desv_mu_mx,True)
desvios.insert(3,"desv_K_N",desv_K_N,True);desvios.insert(4,"desv_Y_NB",desv_Y_NB,True)
desvios.insert(5,"desv_bet_mx",desv_bet_mx,True);desvios.insert(6,"desv_K_S",desv_K_S,True);
desvios.insert(7,"desv_Y_SE",desv_Y_SE,True)

cabeceras_df_desvios = list(desvios.columns.values.tolist())
var_desv = list.copy(cabeceras_df_desvios[2:])

## Bucle ----

for i in var_desv:
    
    
    with plt.style.context({'axes.linewidth': 2.5,
                            'grid.linewidth': 2,
                            'lines.linewidth': 3.0,
                            'lines.markersize': 12,
                            'patch.linewidth': 2,
                            'xtick.major.width': 2.5,
                            'ytick.major.width': 2.5,
                            'xtick.minor.width': 2,
                            'ytick.minor.width': 2,
                            'xtick.major.size': 12,
                            'ytick.major.size': 12,
                            'xtick.minor.size': 8,
                            'ytick.minor.size': 8,
                            'font.size': 50,
                            'axes.labelsize': 24,
                            'axes.titlesize': 24,
                            'xtick.labelsize': 50,
                            'ytick.labelsize': 50,
                            'legend.fontsize': 45,
                            'legend.title_fontsize': 50}):
        
        fig = sns.scatterplot(x="Δt",
                              y=i,
                              hue="error",
                              style="error",
                              edgecolor='b',
                              s = 850,
                              #linewidth=2,
                              #linestyle='--',
                              data=desvios)
    
        plt.grid()                           
        plt.legend(bbox_to_anchor=(1.02, 0.77), title = "E [%]", markerscale=2.,loc='upper left')
        fig.set_xlabel( "Δt [h]", weight='bold', size = 50)
        fig.set_ylabel("%s"%i, weight='bold', size = 50)
        fig.set_title( "%s"%i, weight='bold', size = 50)
    
    figure = plt.gcf()    
    figure.savefig('../Salidas/Desvios/%s.png'%i, dpi = 100, bbox_inches='tight')
    fig.figure.clf()



#%% GRAFICO error_q.global

## Creacion del directorio y armado de objetos necesarios ----

try:
    os.mkdir('../Salidas/Error_q.global')
except:
    pass


## Figura ----

with plt.style.context({'axes.linewidth': 2.5,
                        'grid.linewidth': 2,
                        'lines.linewidth': 3.0,
                        'lines.markersize': 12,
                        'patch.linewidth': 2,
                        'xtick.major.width': 2.5,
                        'ytick.major.width': 2.5,
                        'xtick.minor.width': 2,
                        'ytick.minor.width': 2,
                        'xtick.major.size': 12,
                        'ytick.major.size': 12,
                        'xtick.minor.size': 8,
                        'ytick.minor.size': 8,
                        'font.size': 50,
                        'axes.labelsize': 24,
                        'axes.titlesize': 24,
                        'xtick.labelsize': 50,
                        'ytick.labelsize': 50,
                        'legend.fontsize': 45,
                        'legend.title_fontsize': 50}):
    
    fig = sns.scatterplot(x="Δt",
                          y="err_q.global",
                          hue="error",
                          style="error",
                          edgecolor='b',
                          s = 850,
                          #linewidth=2,
                          #linestyle='--',
                          data=datos)

    plt.grid()                           
    plt.legend(bbox_to_anchor=(1.02, 0.77), title = "E [%]", markerscale=2.,loc='upper left')
    fig.set_xlabel( "Δt [h]", weight='bold', size = 50)
    fig.set_ylabel("Error_q.global", weight='bold', size = 50)
    fig.set_title( "Error_q.global", weight='bold', size = 50)

figure = plt.gcf()    
figure.savefig('../Salidas/Error_q.global/Error_q.global.png', dpi = 100, bbox_inches='tight')
fig.figure.clf()
#%%

