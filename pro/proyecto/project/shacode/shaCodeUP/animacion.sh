#!/bin/bash

# --- Definición de colores ANSI ---
COLOR_ROJO="\033[1;31m"
COLOR_VERDE="\033[1;32m"
COLOR_BLANCO="\033[1;37m"
RESET="\033[0m"

# --- Función de efecto de escritura ---
escribir() {
  local texto="$1" #estos son dos parametros
  local velocidad="${2:-0.0}"  # Velocidad
  # lo tomara como segundo arhgumento, si no, toma valor por defecto
  # en bash los parametros son $1, $2... y se acceden desde el cuerpo


  for (( i=0; i<${#texto}; i++ )); do
    echo -n "${texto:$i:1}"
    sleep $velocidad
  done
  echo
}

