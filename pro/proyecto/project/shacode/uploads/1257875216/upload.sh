#!/bin/bash
source animacion.sh

COLOR_ROJO="\033[1;31m"
COLOR_VERDE="\033[1;32m"
COLOR_BLANCO="\033[1;37m"
RESET="\033[0m"
folder(){
    while [[ ! ($folder == "Y" || $folder == "y" || $folder == "N" || $folder == "n") ]]; do
	echo -e "${COLOR_BLANCO}You can see the folder's ID in your FILES (sha{/}code)${RESET}"
        read -p "[] Save to a folder by ID? [Y/n]: " folder
        if [[ ! ($folder == "Y" || $folder == "y" || $folder == "N" || $folder == "n") ]]; then
            echo -e "${COLOR_ROJO}Invalid input. Please enter 'Y' or 'N'.${RESET}"
        fi
    done
}


after(){
     if [[ $pasa == 0 ]]; then
        nameFile=""
        folderId="z"
	folder="z"

	folder

	if [[ $folder == "Y" || $folder == "y" ]]; then
	    while [[ $folder == "Y" || $folder == "y" ]]; do
	        read -p "[] Folder ID: " folderId
		echo -e "${COLOR_VERDE}Validating data...${RESET}"
		if [[ -z  $folderId || $folderId == "z" ]]; then
		    echo -e "${COLOR_ROJO}Invalid input${RESET}"
		else
		    FOLDER=$(curl -b cookies.txt -s -X POST -H 'Content-type: application/json' -d "{\"folderid\": \"$folderId\"}" "$API_URL/fol")
		    if [[ -z $FOLDER ]]; then
                        echo -e "${COLOR_ROJO}[API Error... ( ˘︹˘ ) ]${RESET}"
                        exit 1
                    fi
		    RESPUESTA=$(echo "$FOLDER" | jq '.respuesta')
		    if [[ $RESPUESTA == "1" ]]; then
		        echo -e "${COLOR_ROJO}Error: folder does not exist${RESET}"
			folderId="z"
			folder="z"
			folder
		    elif [[ $RESPUESTA == "0" ]]; then
		        echo -e "${COLOR_VERDE}The folder was found :)${RESET}"
			echo -e "${COLOR_VERDE}Creating a path to your folder....${RESET}"
			echo -e "${COLOR_VERDE}Server waiting for file {/}${RESET}"
			break
		    fi
		fi
	    done
	fi

        read -p "[] filename or Path: " nameFile
        RESPONSE3=$(curl -b cookies.txt -s -X POST -H 'Content-Type: multipart/form-data' -F "archivo=@$nameFile" -F "folderid=$folderId " "$API_URL/subir")
        if [ -z "$RESPONSE3" ]; then
            echo -e "${COLOR_ROJO}[API error or invalid file... ( ˘︹˘ ) ]${RESET}"
            exit 1
        fi
        mensaje=$(echo "$RESPONSE3" | jq -r '.mensaje')
        mensajeError=$(echo "$RESPONSE3" | jq -r '.error')

        if [[ -n $mensaje ]]; then
            echo -e "${COLOR_VERDE}Success: $mensaje${RESET}"
	    #aqui cierre del programa con exito
	    while IFS= read -r linea; do
	        echo -ne "${COLOR_VERDE}"
                escribir "$linea" 0
		echo -ne "${RESET}"
		sleep 0.0
	    done < arte2.txt
            exit 0
        elif [[ -n $mensajeError ]]; then
            echo -e "${COLOR_ROJO}Upload Failed: $mensajeError${RESET}"
            exit 1
        else
            echo -e "${COLOR_ROJO}Unknown API response: $RESPONSE3${RESET}"
            exit 1
        fi
    fi
}

while IFS= read -r linea; do
    echo -ne "${COLOR_VERDE}"
    escribir "$linea" 0
    echo -ne "${RESET}"
    sleep 0.0
done < arte.txt
echo -e "${COLOR_VERDE}   --- UPLOAD YOUR FILE ---${RESET}"
API_URL="https://silver-barnacle-x55vqwjvgrxpcppp6-5000.app.github.dev"
key_=" "
pasa=1


while [[ ! ($key_ == "Y" || $key_ == "y" || $key_ == "N" || $key_ == "n") ]]; do
    read -p "[] Do you've a special key? [Y/n]: " key_

    # Si la entrada no es válida, mostramos un mensaje de error.
    if [[ ! ($key_ == "Y" || $key_ == "y" || $key_ == "N" || $key_ == "n") ]]; then
        echo -e "${COLOR_ROJO}Invalid input. Please enter 'Y' or 'N'.${RESET}"
    fi
done

# Aquí el bucle ya terminó, por lo que la entrada es válida.
if [[ $key_ == "Y" || $key_ == "y" ]]; then
    echo -e "${COLOR_VERDE}Processing with a special key...${RESET}"
    # Lógica para la opción 'Y'
    key=""
    while true; do
    #read -p "[] Key: " key

    gcc kReader.c -o krs

    ./krs
    file=".tmp.txt"
    if [[ ! -f $file ]]; then
        echo "error internal key :("
	exit 1
    fi
    key=$(cat $file)

    trap 'rm -f $file' EXIT
    trap 'rm -f krs' EXIT

    if [[ -z $key ]]; then
         echo -e "${COLOR_ROJO}Error: Key  must be provided. Please try again.${RESET}"
         continue
    fi
    echo -e "${COLOR_VERDE}processing your key...${RESET}"
    echo -e "${COLOR_VERDE}[waiting for response from server]...${RESET}"

    # 1. Enviar la solicitud POST a la API y guardar la respuesta en una variable.
    # La opción -s (silent) evita que curl imprima información de progreso.
    # La opción -d (data) envía el valor como un JSON.
    RESPONSE=$(curl -c cookies.txt -s -X POST -H "Content-Type: application/json" -d "{\"valor\": \"$key\"}" "$API_URL/llave_")

    if [ -z "$RESPONSE" ]; then
        echo -e "${COLOR_ROJO}[API Error... ( ˘︹˘ ) ]${RESET}"
        exit 1
    fi
    # 3. Usar 'jq' para extraer el valor del campo 'resultado'.
    # El comando 'jq' toma el JSON de la variable $RESPONSE y devuelve el valor de .resultado.
    # Si 'jq' no está instalado, esto fallará.
    RESULTADO=$(echo "$RESPONSE" | jq '.resultado')
    NAME=$(echo "$RESPONSE" | jq -r '.name')

    # 4. Usar un if/else para tomar una decisión basada en el valor.
    if [ "$RESULTADO" == "1" ]; then
        # llave autentificada
	# seria cheto algo como "se verifico la llave\n hola 'username'!!"

	echo -e "${COLOR_VERDE}The value was successfully verified (code: 200).${RESET}"
	echo -e "${COLOR_VERDE}HI, ${RESET}${COLOR_BLANCO}$NAME!!${RESET}${COLOR_VERDE} Complete validation${RESET}"
        echo -e "${COLOR_VERDE}Ready to upload your file...${RESET}"
        # Lógica que se ejecuta si el resultado es 1
	pasa=0
        break

    elif [ "$RESULTADO" == "0" ]; then
        echo -e "${COLOR_ROJO}The value did not pass verification (code: 400).${RESET}"
        #el resultado no es el esperado
    else
        echo -e "${COLOR_ROJO}[Error: Unexpected API response... ( ˘︹˘ ) ] Result code: $RESULTADO${RESET}"
        #la API retorno algun otro valor
    fi
    done
    after

# si no hay llave especial
# es decir respueesta 'N'
else
    echo -e "${COLOR_VERDE}Processing without a special key...${RESET}"
    while true; do
        while true; do
	    username=""
	    password=""
            read -p "[] Username: " username

	    gcc psReader.c -o prs

	    ./prs
     	    file=".tmp.txt"
	    if [[ ! -f $file ]]; then
	        echo "password internal error :("
		exit 1
	    fi
	    password=$(cat $file)

	    trap 'rm -f $file' EXIT
            trap 'rm -f prs' EXIT
            echo "-----------...-------------"
            if [[ -z $username || -z $password ]]; then #tener en cuenta la difencia de un if []; y un if [[]]; son parecidos pero distintos
                echo -e "${COLOR_ROJO}Error: Both username and password must be provided. Please try again.${RESET}"
            else
                echo -e "${COLOR_VERDE}Credentials received. Continuing...${RESET}"
 		    break
                    # Salimos del bucle cuando la entrada es válida
            fi
	done

	#ahora se hace una verificacion de existencia del usuario y password
        RESPONSE2=$(curl -c cookies.txt -s -X POST -H "Content-Type: application/json" -d "{\"user\": \"$username\", \"password\": \"$password\"}" "$API_URL/veri")

	if [ -z "$RESPONSE2" ]; then
            echo -e "${COLOR_ROJO}[API Error... ( ˘︹˘ ) ]${RESET}"
            exit 1
        fi

	RESULTADO2=$(echo "$RESPONSE2" | jq '.resultado')
        if [[ $RESULTADO2 == "1" ]]; then
            echo -e "${COLOR_VERDE}The user is valid :)${RESET}"
	    pasa=0
            break #se completa
        elif [[ $RESULTADO2 == "2" ]]; then
            echo -e "${COLOR_ROJO}invalid password ( ˘︹˘ )${RESET}"
        elif [[ $RESULTADO2 == "3" ]]; then
            echo -e "${COLOR_ROJO}invalid username ( ˘︹˘ )${RESET}"
        fi
    done
    after
fi
