#!/bin/bash

# Ruta de la carpeta principal que contiene las subcarpetas
carpeta_principal="/home/franco/Escritorio/Repos/Funciones Varias/Efecto_Muestreo/Run03_re-ejecuciones_todo_nuevosDatos"

# Iterar sobre todas las subcarpetas
for subcarpeta in "$carpeta_principal"/*; do
  # Verificar si es una carpeta
  if [ -d "$subcarpeta" ]; then
    # Borrar todos los archivos, excepto los llamados "0_Resutls_Abstract.csv"
    find "$subcarpeta" ! -name "0_Resutls_Abstract.csv" -type f -exec rm -f {} +
  fi
done

