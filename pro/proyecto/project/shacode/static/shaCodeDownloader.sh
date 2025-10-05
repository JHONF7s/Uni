#!/bin/bash

API_URL=""

COLOR_ROJO="\033[1;31m"
COLOR_VERDE="\033[1;32m"
COLOR_BLANCO="\033[1;37m"
RESET="\033[0m"

read -p "API_URL: " API_URL
echo -e "${COLOR_VERDE}$API_URL${RESET}"

if [[ -z $API_URL ]]; then
    API_URL="https://silver-barnacle-x55vqwjvgrxpcppp6-5000.app.github.dev"
fi

echo -e "${COLOR_VERDE}Sending request to server..${RESET}"
echo -e "${COLOR_VERDE}Downloading Files${RESET}"

curl --progress-bar -OJ -X GET "$API_URL/download-sha-down"
if [[ $? -ne 0 ]]; then # -ne = not equal
    echo -e "${COLOR_ROJO}API Error... ( ˘︹˘ )${RESET}"
    echo -e "${COLOR_ROJO}Download Failed: try again${RESET}"
    exit 1
fi
RUTA=$(pwd)

unzip shaCodeDOWN.zip
rm -f shaCodeDOWN.zip
cd shaCodeDOWN
chmod +x download.sh
chmod +x animacion.sh
echo "alias down=\"bash $RUTA/shaCodeDOWN/download.sh\"" >> $HOME/.bashrc
cd ..
curl --progress-bar -OJ -X GET "$API_URL/download-sha-up"
if [[ $? -ne 0 ]]; then
    echo -e "${COLOR_ROJO}API Error... ( ˘︹˘ )${RESET}"
    echo -e "${COLOR_ROJO}Download Failed: try again${RESET}"
    exit 1
fi
unzip shaCodeUP.zip
rm -f shaCodeUP.zip
cd shaCodeUP
chmod +x upload.sh
chmod +x animacion.sh
echo "alias up=\"bash $RUTA/shaCodeUP/upload.sh\"" >> $HOME/.bashrc
cd ..

source ~/.bashrc
echo -e "${COLOR_VERDE}Download completed Successfully :)${RESET}"
echo -e "${COLOR_VERDE}You can type${RESET} ${COLOR_BLANCO}up${RESET} ${COLOR_VERDE}or${RESET} ${COLOR_BLANCO}down${RESET} ${COLOR_VERDE}on the command line :)${RESET}"
echo -e "${COLOR_BLANCO}run 'source ~/.bashrc' for added security${RESET}"
sleep 1
rm -f shaCodeDownloader.sh
# " " permite usar variables de forma dinamica
# ' ' trata todo como texto
