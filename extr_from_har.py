#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 16 21:54:33 2023

#########################
#                       #
# Extraccion de audios  #
# Desde .har (genially) #
#                       #
#########################

@author: Franco Neme
"""
#%% CARGA DE LIBRERIAS
# = = = = = = = = = = = =

import json
import os
import subprocess
from urllib.parse import urlparse


#%% DESCARGA DE ARCHIVOS .MP3 DESDE .HAR
# = = = = = = = = = = = = = = = = = = = = 

def descargar_archivo(url, nombre):
    subprocess.call(["curl", "-O", url])
    print(f"Descargado: {nombre}")

def extraer_archivos_mp3(archivo_har):
    with open(archivo_har, 'r') as archivo:
        har_data = json.load(archivo)
    
    entradas = har_data['log']['entries']
    for entrada in entradas:
        url = entrada['request']['url']
        if url.endswith('.mp3'):
            nombre = os.path.basename(urlparse(url).path)
            descargar_archivo(url, nombre)

archivo_har = 'view.genial.ly.har'  # Reemplaza con la ruta y nombre de tu archivo .har
extraer_archivos_mp3(archivo_har)



#%% RENOMBRAMIENTO DE ARCHIVOS
# = = = = = = = = = = = = = = =

def renombrar_archivos_mp3(carpeta):
    archivos_mp3 = [archivo for archivo in os.listdir(carpeta) if archivo.endswith('.mp3')]
    archivos_mp3.sort(key=lambda x: os.path.getctime(os.path.join(carpeta, x)))

    for indice, archivo in enumerate(archivos_mp3, start=1):
        nuevo_nombre = f"audio {indice}.mp3"
        ruta_antigua = os.path.join(carpeta, archivo)
        ruta_nueva = os.path.join(carpeta, nuevo_nombre)
        os.rename(ruta_antigua, ruta_nueva)
        print(f"Renombrado: {archivo} -> {nuevo_nombre}")

carpeta_descargas = os.getcwd() # Reemplaza con la ruta de la carpeta donde se encuentran las descargas
renombrar_archivos_mp3(carpeta_descargas)


#%%
