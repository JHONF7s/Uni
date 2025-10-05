# Final Project - ShaCode by JHONF7
#### Video Demo: <URL>
#### Description:
Este proyecto esta lleno de novedades y de
funcionalidades mas alla de ser una simple app web
que se pueda abrir desde un motor de busqueda.

Se le estuvo mostrando a ClaudeIA las partes mas relevantes de este
proyecto y ella lo define como:
```

┌─────────────────────────────────────────────┐
│         FILE COLLABORATION PLATFORM         │
├─────────────────────────────────────────────┤
│ 🌐 Full Web Management Interface            │
│ 📡 REST API (CLI + automation)              │
│ ⚡ Real-time Collaborative Editor           │
│ 🛠️ Professional CLI Distribution            │
│ 🔐 Advanced Granular Authentication         │
│ 📋 Permission & Access Control System       │
│ 👥 User Discovery & Social Sharing          │
│ 📊 File Metadata & Activity Analytics       │
└─────────────────────────────────────────────┘
```

De que trata ShaCode? Es una app en la cual puedes
subir archivos, carpetas y no solo subir, tambien
crearlas, ademas, como si fuera poco, puedes tambien
descargarlos, en resumen, ShaCode fue pensado como
una pequena nube en la cual puedas subir tus
archivos (especialmente codigo) ya que ShaCode nace como
idea mia de la palabra "shared code" lo que puedes hacer en
esta app es un poco extenso, me tome el tiempo para pensar algunos
requerimientos funcionales interesantes, para que ShaCode no solo se quedara como
un proyecto academico, sino tambien como un proyecto personal para
gestionar mis propios archivos y codigos durante mi formacion academica en
mi universidad y en CS50, uno de los usos que son mas destacables merecen ser listados:

1. crear una cuenta
2. crear una llave especial para hacer login (mas adelante nombrare sus usos)
3. subir archivos desde la app
4. subir archivos desde una consola (linux)
5. descargar archivos desde la app
6. descargar archivos desde una consola (linux)
7. compartir archivos con otros usuarios
8. determinar un nivel de acceso al compartir un archivo
9. eliminar un permiso
9. editar o leer archivos si eres el usuario a quien le compartieron un archivo o carpeta
10. editar tus archivos (preferiblemente de codigo para no romper formatos)
11. eliminar archivos
12. renombrar archios
13. consultar tu informacion
14. consultar informacion sobre cada archivo
15. consultar informacion de otros usuarios filtrando por nombre
16. consultar informacion de los archivos que has compartido
17. consultar informacion de los archivos que te han compartido
18. puedes configurar tu informacion
19. puedes cambiar de clave especial (el sistema te genera varias de forma creativa)
20. puedes cerrar sesion

Estas 20 cosas hacen parte del corazon del proyecto, aun asi no son lo unico
solo quise hacer una lista que resuma en esencia lo que se quiere lograr con la app, ahora si
hablaremos de estos puntos, por lo menos los menos explicitos para explicar de forma tecnica
o intuitiva su funcionamiento interno y su uso, especailmente de como funcionan los programas
de consola hechos adicionalmente para este mismo proyecto para interactuar con la API sin que
sea necesario ingresar a la app en un caso en el que necesites ingresar a un archivo, la unica
limitacion de estos mismo Scripts es que solo funcionan desde una consola linux, aun asi la
app bien se puede acceder desde cualquier navegador.


## Como Funciona ShaCode
Desde un punto de vista mas tecnico, el servidor por defecto de flask fue cambiado
por SocketIO para poder usar el poder de los elementos bidireccionales que practicamente
permiten que el usuario reciba informacion en tiempo real desde el servidor, a esto se le conoce
como un "apreton de manos", donde el servidor y el usuario se envian datos mutuamente, esto es mucho
mejor cuando se busca dar una experiencia online genuina, ya que ya no todo va a depender uniacmente
de las solicitudes HTTP/HTTPS a pesar de que tambien son un punto muy importante.

En el directorio `project` tenemos la siguiente estructura:
```
project/
├── shaCode/
│   ├── app.py
|   ├── shaCodeUp/
|   ├── helpers.py
│   ├── requirements.txt
│   ├── shacode_.db
│   ├── templates/
│   ├── static/
│   └── uploads/
├── README.md
```


### App and Web Interfaces
Aqui podemos hace un analisis rapido de lo que esta pasando, `app.py` es el
corazon para que todo funcione, en `templates/` esta todo lo necesario para que
el frontend funcione con un estilo minimalista, `helpers.py` tiene todo lo
necesario como funciones y demas para funcionamientos especificos abstraidos y
demas, me hubiese gustado abstraer mas funciones para hacer un codigo mas limpio
pero como soy el unico trabajando en esto, se vuelve tedioso, aun asi espero
hacerlo en los proximos dias como tarea personal.

Aun asi se logro un estilo y funcionamiento optimo en funcion con la base de
datos y la logica lograda que satisface los requerimientos del proyecto
el estilo fue inspirado en la tarea de la semana 9 llamado Finance, pero
en ShaCode se opta por un estilo gris y oscuro.


### Usuarios
Esta parte es simple, pero interesante para entender como se gestionan los archivos
como funcionan los Script y al mismo tiempo como se protegen los archivos de otros
usuarios frente a que tan accesible es un archivo de otro usuario con el Scrip
para descargar archivos desde la consola de linux, pues cuando un usuario se registra
solo necesita nombre y su clave, pero hay algo mas que el usuario puede hacer despues
de registrarse, y eso es, crear una llave especial, esta se crea por defecto, pero,
que pasa si quieres cambiar de llave especial? Pues facil, solo ingresas una palabra
aleatoria y esta crea una llave especial diferente, donde aqui depende de tu aleatoriedad

```
@app.route("/changeSpecialKey", methods=["POST"])
@login_required
def chan():
    user_id = session["user_id"]
    hash = request.form.get("hash")
    key = simpleHash(user_id, hash)

    db.execute("DELETE FROM keys WHERE user_id = ?", user_id)
    db.execute("INSERT INTO keys (user_id, key) VALUES (?, ?)", user_id, key)

    flash("Generated special Key!! ___ It's unique per user, don't share it ________  ദ്ദി(ᵔᗜᵔ) ")
    return redirect("/profile")
```
Este endpoint es una prueba de como funciona esta parte de como quieres cambiar
tu llave, siendo `hash` la palabra que ingresas, y la funcion simpleHash una forma
sencilla de generar un numero hexadecimal para esta misma llave especial, en `app.py`
estan los otros `endpoints` relacionados por si deseas verlos.

Pero entonces, por que es tan importante? cuando quieras descargar o subir algo desde la
consola podras usarla llave o tu usuario, pero la llave hara que esta tarea sea bastante
rapido ya que las llaves suelen verse como `b845` ademas con la posibilidad de crear,
eliminar y cambiarlas a tu gusto, util por si quieres darle acceso temporal a otro usuario
para cualquier caso sin tener que dar tu password, y con la libertad de cambiarla o
eliminarla cuando quieras.


### CLI linux
Aqui es donde el usuario interactua con la API, por ejemplo, desde una consola
linux puedes ejecutar:
```
curl -# -OJ <URL>/download-sha
```
Donde `download-sha` es el endpoint que recibira la solicitud y como respuesta
enviara un archivo:
```
 try:
        return send_file(
            path,
            as_attachment=True,
            download_name='shaCodeDownloader.sh'
        )
    except FileNotFoundError:
        return "file does not exist :(", 404
```
Donde `shaCodeDownloader.sh` es un Script bash que automatiza la instalacion
de los Scripts que te permiten subir y bajar archivos desde la consola y no
solo los descarga, crea un alias para estos y se autodestruye, haciendo que
el usuario no tenga necesidad de volver a escribir ninguna solicitud curl ni
cambios tecnicos en archivos como `~/.bashrc`.

Contenido del Script:
```

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
```


Se muestra esto para dar prueba de los Scripts que automatizan el trabajo desde
la consola haciendo mucho mejor la forma en la que interactua el usuario, si
quieres ver los otros Scripts, estos se encuentran en `static/` son dos archivos
.zip que si descomprimes veras varios archivos `.sh` y algunos `.c` ya que se
agregaron animaciones de consola basicas, pero divertidas.

Por ultimo el usuario por medio de comandos como `up` y `down` podra interactuar
con el API para subir y bajar archivos usando `users`y `password` o por
medio de una `clave especial` para que el servidor sepa quien eres y puedas
descargar algun archivo o carpeta por medio de un ID el cual el usuario puede ver
desde la aplicacion web.


### Codigo Colavorativo
Como se menciono antes le puedes compartir archivos a otros usuarios, si
compartes un archivo, por ejemplo, `hola.c` a un amigo como `editor` ambos podran
editar al mismo tiempo y poder ver los cambios en tiempo real, esto gracias
a SocketIO, el endpoint que demuestra esto:
```

@socketio.on('textUpdate')
def handle_text_update(data):
    file_id = data.get('file_id')
    content = data.get('content', '')
    file = db.execute("SELECT * FROM files WHERE id = ?", file_id)

    pathFile = os.path.join(
        app.config["UPLOAD_FOLDER"],
        str(file[0]["user_id"]),
        build_file_path(str(file_id))
    )

    try:
        with open(pathFile, "w", encoding="utf-8") as f:
            f.write(content)
        emit('textUpdate', {'file_id': file_id,
                            'content': content,
                            'sender': request.sid},
                            broadcast=True,
                            include_self=False)
    except Exception as e:
        emit('error', {'message': str(e)})

```
Aqui el elemento `data` es enviado desde el editor gracias a JavaSript, no se
indagara a mucho detalle, pero aqui lo que pasa es que al objeto `data` se le
extre su contenido y el file_id, gracias a este se consulta el archivo en
la base de datos, denido a que el file tiene un propietario quien a su vez
tiene un ID, el cual en el directorio `uploads` es la clave principal de como
se organizan los archivos para cada usuario de forma ordenada ya que el ID es
inmutable y ademas unico, por eso mismo `pathFile` representa la ruta absoluta
del archivo que se esta editando, sin importar quien lo hizo (porque lo mas
seguro es que el editor sea el propietario o tenga los permisos necesarios),
luego este archivo se abre y se escribe el contenido al archivo fisico y por
ultimo se emite este cambio a todos los usuarios que estan en el servidor, menos
al que lo envio.


### Permisos y Compartidos
Desde la app web puedes ver todos los archivos que compartiste y te han
compartido desarrollar esta parte fue dificil y aun asi faltan cosas por
abstraer o refactorizar, el problema mas grande fue el siguiente, teniendo
en cuenta el esquema de la base de datos para los permisos:
```

CREATE TABLE permissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,         -- el usuario que recibe el permiso
    file_id INTEGER,                  -- puede ser NULL si es para una carpeta
    folder_id INTEGER,                -- puede ser NULL si es para un archivo
    access_level TEXT NOT NULL,       -- 'reader', 'editor'
    puser_id INTEGER NOT NULL,        -- usuario propietario
    FOREIGN KEY (puser_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (file_id) REFERENCES "files"(id) ON DELETE CASCADE,
    FOREIGN KEY (folder_id) REFERENCES "folders"(id) ON DELETE CASCADE
);
```
Como se ve en el esquema anterior, una carpeta o archivo se comparte por medio
de un `ID`, pero aqui surge la siguiente pregunta: si un usuario tiene acceso
como editor a una carpeta, podria editar los archivos en su interior?

Creo que la respuesta mas obvia es que, SI, pero entonces, si desde la tabla
`permissions` solo puedo extraer informacion muy superficial, como por ejemplo
el `folder_id` y el usuario con acceso, como extraigo los `file_id` y `folder_id`
en los cuales el usuario tiene permisos de una forma abstracta debido a que no
estan explicitos en la base de datos? esta necesidad surge porque el acceso al
editar, descargar o leer un archivo es por medio de los `file_id` de los mismos
entonces el problema se convirtio un problema de coherencia, donde la pregunta
principal fue `si compartes una carpeta, como puedes usar este folder_id de la
base de datos para identificar todos los archivos y carpetas que estas
compartiendo?` aqui hacer cambios bruscos en la base de datos no era una opccion
pues eso implica cambiarlo todo, asi que como solucion, se implemento la
siguiente funcion:
```

def hayPermisoFC(id, user_id, modo):
    folderID = id
    while folderID != None:
        folder = db.execute("SELECT * FROM folders WHERE id = ?", folderID)
        if folder:
            permiso = db.execute("""SELECT * FROM permissions WHERE
                                 folder_id = ?
                                 AND user_id = ?
                                 AND access_level = ?""", folder[0]["id"], user_id, modo)
            if permiso:
                return True
            folderID = folder[0]["parent_id"]
        else:
            break
    return False
```

Esta solucion permitio sanar esta herida de una forma rapida, para entender lo
que pasa hay que echarle un ojo al esquema de las carpetas en la base de datos
```
CREATE TABLE IF NOT EXISTS "folders" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    parent_id INTEGER,
    is_private BOOLEAN DEFAULT 1,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (parent_id) REFERENCES "folders"(id) ON DELETE CASCADE
);
```
Como se puede ver una carpeta no solo tiene un ID, sino tambien un `parent_id`
para las carpetas madres que contienen a otras, al igual que el esquema de los
archivos, pues estos tienen un `folder_id` que indica el id de la carpeta donde
se encuentran
```
CREATE TABLE IF NOT EXISTS "files" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    filepath TEXT NOT NULL,
    folder_id INTEGER,
    user_id INTEGER NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_private BOOLEAN DEFAULT 1,
    FOREIGN KEY (folder_id) REFERENCES "folders"(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```
Como se puede ver hasta el momento mostrando estos esquemas, ya podemos tocar el
corazon de los archivos compartidos en ShaCode, pues vemos que todo esta
relacionado entre si, entonces ya podemos comprender mejor la funcion
`hayPermiso()` anteriormente presentada, pues lo que se hace es buscar en las
carpetas madres de un archivo hasta llegar a la que tiene el permiso filtrando
con mas datos, si se llega a una carpeta madre con permisos retorna `true`, pero
si la carpeta madre ya no tiene ningun permiso y ademas no tiene una madre a la
cual le podamos preguntar, es decir que el `parent_id` sea nulo, entonces retorna
`false`.


Siguiendo esta misma logica en la cual una carpeta y archivo se ubica por
carpetas madr, pues ya podemos generar carpetas que de forma recursiva o
conveniente pueda listar todo su contenido, o sea a lo que tienes acceso o a lo
que diste acceso, entonces gracias a esta forma de gestionar archivos podemos
generar una plantilla `html` en la app para que veas todo lo que te `compartieron`
y `compartiste`, como podras imaginarte, esto generaba dificultad con las carpetas
con los archivos individuales es mas directo y consume menos recursos.
