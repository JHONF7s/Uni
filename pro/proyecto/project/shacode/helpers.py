import requests
import os
from cs50 import SQL
from flask import redirect, render_template, session
from functools import wraps

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///shacode_.db")
db.execute("PRAGMA foreign_keys = ON")

def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def lookup(symbol):
    """Look up quote for symbol."""
    url = f"https://finance.cs50.io/quote?symbol={symbol.upper()}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for HTTP error responses
        quote_data = response.json()
        return {
            "name": quote_data["companyName"],
            "price": quote_data["latestPrice"],
            "symbol": symbol.upper()
        }
    except requests.RequestException as e:
        print(f"Request error: {e}")
    except (KeyError, ValueError) as e:
        print(f"Data parsing error: {e}")
    return None


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"



#my
def build_folder_tree(folders):
    tree = []
    lookup = {}

    for folder in folders:
        folder["children"] = []
        lookup[folder["id"]] = folder

    for folder in folders:
        parent_id = folder["parent_id"]
        if parent_id:
            lookup[parent_id]["children"].append(folder)
        else:
            tree.append(folder)
    return tree


def archi(folders, files):
    tree = {}
    tree["folders"] = []
    tree["files"] = []
    lookup = {}

    for folder in folders:
        folder["children"] = []
        folder["childrenFile"] = []
        lookup[folder["id"]] = folder


    for file in files:
        id = file["folder_id"]
        if id:
            lookup[id]["childrenFile"].append(file)
        else:
            tree["files"].append(file)

    for folder in folders:
        parent_id = folder["parent_id"]
        if parent_id:
            lookup[parent_id]["children"].append(folder)
        else:
            tree["folders"].append(folder)
    return tree


def build_folder_path(folder_id):
    if folder_id:
        path_parts = []
        while folder_id:
            folder = db.execute("SELECT * FROM folders WHERE id = ?", folder_id)
            if folder:
                path_parts.insert(0, folder[0]["name"])
                folder_id = folder[0]["parent_id"]

        if path_parts:
            return os.path.join(*path_parts)
        else:
            return ""
    else:
        return ""


def build_file_path(file_id):
    file = db.execute("SELECT * FROM files WHERE id = ?", file_id)
    name = file[0]["filename"]
    pid = file[0]["folder_id"]
    path = build_folder_path(pid)
    return os.path.join(path, name)





def hacerCarpeta(id):
    #guardamos todo sin jerarquia
    allFolders = []

    # Obtener la carpeta raíz explícita
    raiz = db.execute("SELECT * FROM folders WHERE id = ?", id)
    if raiz:
        raiz[0]["parent_id"] = None
        allFolders.append(raiz[0])

    allFiles = []
    #se extraen las carpetas hijas
    hijas = db.execute("SELECT * FROM folders WHERE parent_id = ?", id)

    for folder in hijas: # se recorren las hijas
        allFolders.append(folder) # se agrega a la lista
        subfolder, subfile = hacerCarpeta(folder["id"]) #llamada recursiva

        allFolders.extend(subfolder)
        allFiles.extend(subfile) # extend agrega a la lista principal

    # se buscan a todos los archivos en la carpeta actual
    files = db.execute("SELECT * FROM files WHERE folder_id = ?", id)
    allFiles.extend(files)
    return allFolders, allFiles # retorno de las dos listas



def jerarquia(folders, files):

    tree = archi(folders, files)
    return tree




def archi2(folders, files, root_id):
    # Preparar lookup con nodos vacíos
    lookup = {
        f["id"]: {
            **f,
            "children": [],
            "childrenFile": []
        }
        for f in folders
    }

    # Asignar archivos a su carpeta
    tree_files = []
    for file in files:
        pid = file["folder_id"]
        if pid in lookup:
            lookup[pid]["childrenFile"].append(file)
        else:
            # opcional: archivos sin carpeta valida
            tree_files.append(file)

    # Anidar carpetas hijas bajo sus padres
    for f in folders:
        pid = f["parent_id"]
        if pid in lookup:
            lookup[pid]["children"].append(lookup[f["id"]])

    # solo la carpeta raíz entra en tree["folders"]
    tree_folders = []
    if root_id in lookup:
        tree_folders.append(lookup[root_id])

    return {
        "folders":   tree_folders,
        "files":     tree_files
    }



def simpleHash(numero, hash):
    if hash:
        resultado = 0
        for char in hash:
            resultado += ord(char) * 1187
        for num in str(numero):
            resultado += int(num) * 1097
        return hex(resultado)[2:] # slicing
    else:
        resultado = 0
        for num in str(numero):
            resultado += int(num) * 1097
        return hex(resultado)[2:] # slicing





def mode(filename):
    extension_map = {
        "py": "python", "js": "javascript", "html": "htmlmixed", "css": "css",
        "java": "text/x-java", "c": "text/x-csrc", "cpp": "text/x-c++src", "cs": "text/x-csharp",
        "php": "php", "rb": "ruby", "go": "go", "rs": "rust", "md": "markdown",
        "sql": "sql", "sh": "shell", "xml": "xml", "yml": "yaml", "json": "application/json",
        "tex": "stex", "pl": "perl", "lua": "lua", "swift": "swift", "scala": "scala",
        "kt": "kotlin", "dart": "dart", "hs": "haskell", "clj": "clojure", "ex": "elixir",
        "erl": "erlang", "pas": "pascal", "vb": "vb", "v": "verilog", "vhd": "vhdl",
        "conf": "nginx", "dockerfile": "dockerfile", "proto": "protobuf", "tcl": "tcl",
        "twig": "twig", "pug": "pug", "hbs": "handlebars", "sass": "sass",
        "scss": "scss", "less": "less", "sh": "shell"
        }
    if filename.lower() == "dockerfile":
        return "dockerfile"


    modeExtension = filename.lower().rsplit('.', 1)[-1] if '.' in filename else ''
    # 1 significa la cantidad de divisiones por la derecha y -1 el ultimo elemento
    mode = extension_map.get(modeExtension, "plaintext")
    return mode




def es_entero(valor):
    try:
        int(valor)
        return True
    except ValueError:
        return False

# este sirve para confirma de forma casi que "recursiva" si el usuario tiene permiso en una subcarpeta o subarchivo
def hayPermiso(file, user_id):
    folderID = file[0]["folder_id"]
    while folderID != None:
        folder = db.execute("SELECT * FROM folders WHERE id = ?", folderID)
        if folder:
            permiso = db.execute("""SELECT * FROM permissions WHERE
                                 folder_id = ?
                                 AND user_id = ? """, folder[0]["id"], user_id)
            if permiso:
                return True
            folderID = folder[0]["parent_id"]
        else:
            break
    return False


# este se usa para verificar un modo en especifico, es muy importante para el script desde la consola
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




def addMetadatos(item, permisosUsuario, permisoActual, tipoItem):
    usuarioPropietario = db.execute("SELECT username FROM users WHERE id = ?", permisoActual["puser_id"])
    if usuarioPropietario:
        item["shared_by"] = usuarioPropietario[0]["username"]
        item["access"] = permisoActual["access_level"]
        permisosUsuario[tipoItem].append(item)



def sizeCarpeta(ruta):
    total = 0
    # D = directorio
    for Dactual, Dsub, fileNames in os.walk(ruta):
        for file in fileNames:
            ruta = os.path.join(Dactual, file)
            if os.path.isfile(ruta):
                total += os.path.getsize(ruta)
    return total


