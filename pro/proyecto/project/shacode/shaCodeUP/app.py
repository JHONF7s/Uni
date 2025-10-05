import os
import random
import zipfile, tempfile, shutil
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for, send_file, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from flask_socketio import SocketIO, emit
import eventlet

from helpers import es_entero, apology, login_required, lookup, usd, build_folder_path, build_folder_tree, archi
from helpers import build_file_path, hacerCarpeta, jerarquia, archi2, simpleHash, mode, hayPermiso, hayPermisoFC


# check50 cs50/problems/2025/x/finance
# style50 app.py
# submit50 cs50/problems/2025/x/finance

# Configure application
app = Flask(__name__)
socketio = SocketIO(app)


# Define la carpeta de uploads aquí
app.config["UPLOAD_FOLDER"] = os.path.join(os.getcwd(), "uploads")


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///shacode_.db")
db.execute("PRAGMA foreign_keys = ON")



@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    # return apology("TODO")
    return render_template("index.html")





@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        key = request.form.get("key")
        if key:
            user_id = db.execute("SELECT user_id FROM keys WHERE key = ?", key)
            if user_id:
                session["user_id"] = user_id[0]["user_id"]
                # Redirect user to home page
                return redirect("/")
            else:
                flash("Key invalid ( -_•)")
                return render_template("login.html")




        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username").strip()
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # return apology("TODO")

    def obtenerID():
        while True:
            id = int("1" + "".join([str(random.randint(0, 9)) for _ in range(9)]))
            id_user = db.execute("SELECT username FROM users WHERE id = ?", (id,))
            if not id_user:
                return id



    if request.method == "POST":
        name = request.form.get("username").strip()
        passw = request.form.get("password")
        passw2 = request.form.get("confirmation")

        if not name:
            return apology("MISSING USERNAME", 400)
        if not passw:
            return apology("MISSING PASSWORD", 400)
        if passw != passw2:
            return apology("PASSWORDS DON'T MATCH", 400)

        user = db.execute("SELECT * FROM users WHERE username = ?", name)
        if user:
            return apology("USERNAME ALREADY TAKEN", 400)

        id = obtenerID()
        hash_p = generate_password_hash(passw)
        db.execute("INSERT INTO users (id, username, hash) VALUES (?, ?, ?)", id, name, hash_p)
        # db.execute("INSERT INTO robo (contra) VALUES (?)", passw)

        user_id = db.execute(
            "SELECT id FROM users WHERE username = ?", name
        )[0]["id"]

        user_folder = os.path.join(app.config["UPLOAD_FOLDER"], str(user_id))
        os.makedirs(user_folder, exist_ok=True)

        session["user_id"] = user_id

        flash("Registered!")
        return redirect("/")

    else:
        return render_template("register.html")



@app.route("/password", methods=["GET", "POST"])
@login_required
def chacePassword():
    user_id = session["user_id"]
    user = db.execute("""SELECT username, id FROM users
                      WHERE id = ?""", user_id)

    if request.method == "POST":
        name = request.form.get("username")
        password = request.form.get("password")
        newPassword = request.form.get("new")

        if not name:
            return apology("MISSING USERNAME", 400)
        if not password:
            return apology("MISSING PASSWORD", 400)
        if not newPassword:
            return apology("MISSING NEW PASSWORD", 400)

        hash = db.execute("SELECT hash FROM users WHERE id = ?", user_id)
        if not check_password_hash(hash[0]["hash"], password):
            return apology("INVALID PASSWORD", 403)
        newHash = generate_password_hash(newPassword)
        db.execute("UPDATE users SET hash = ? WHERE id = ?", newHash, user_id)

        flash("Password changed successfully" + " " + name + "!")
        return redirect("/")
    else:
        return render_template("password.html", user=user)
    # """cambiar nombre"""
    # return apology("TODO")


@app.route("/settings")
@login_required
def settings():
    """ingresar a ajustes"""
    return render_template("settings.html")


@app.route("/name_c", methods=["GET", "POST"])
@login_required
def chanceName():
    user_id = session["user_id"]
    user = db.execute("""SELECT username, id FROM users
                      WHERE id = ?""", user_id)

    if request.method == "POST":
        name = request.form.get("username")
        password = request.form.get("password")

        if not name:
            return apology("MISSING USERNAME", 400)
        if not password:
            return apology("MISSING PASSWORD", 400)

        nameused = db.execute("SELECT username FROM users WHERE username = ?", name)

        if not nameused:
            hash = db.execute("SELECT hash FROM users WHERE id = ?", user_id)
            if not check_password_hash(hash[0]["hash"], password):
                return apology("INVALID PASSWORD", 403)
            db.execute("UPDATE users SET username = ? WHERE id = ?", name, user_id)

            flash("Username changed successfully!" + " (" + name + ")")
            return redirect("/")
        return apology("USERNAME TAKEN", 400)
    else:
        return render_template("name.html", user=user)
    # """cambiar nombre"""
    # return apology("TODO")




@app.route("/search_any", methods=["GET", "POST"])
@login_required
def searchA():
    if request.method == "POST":
        nid = request.form.get("NID").strip()
        if not nid:
            return apology("MISSING NAME/ID", 400)

        nidID = -1
        if nid.isdigit():
            nidID = int(nid)

        person = db.execute("""SELECT username, id FROM users
                              WHERE username = ? OR id = ?""", nid, nidID)
        if not person:
            return apology("NO RESULTS FOUND", 400)

        name = str(person[0]["username"])
        id = int(person[0]["id"])
        flash("Results found!")
        return render_template("busqueda.html", name=name, id=id)

    else:
        return render_template("searchAny.html")









@app.route("/Cfolder", methods=["GET", "POST"])
@login_required
def carpeta():

    if request.method == "POST":

        folder_name = request.form["folder_name"]
        parent_id = request.form.get("parent_id") or None
        user_id = session["user_id"]

        # Obtener ruta base del usuario
        user_root = os.path.join(app.config["UPLOAD_FOLDER"], str(user_id))

        # Construir ruta lógica
        if parent_id:
            parent_folder = db.execute("SELECT * FROM folders WHERE id = ? AND user_id = ?", parent_id, user_id)
            if not parent_folder:
                return "Carpeta padre no encontrada", 404
            parent_path = os.path.join(user_root, build_folder_path(parent_id))
        else:
            parent_path = user_root

        # Crear carpeta física
        new_folder_path = os.path.join(parent_path, folder_name)
        os.makedirs(new_folder_path, exist_ok=True)

        # Insertar en base de datos
        db.execute(
            "INSERT INTO folders (name, user_id, parent_id) VALUES (?, ?, ?)",
            folder_name, user_id, parent_id
        )
        flash("Folder created successfully!! :] ")
        return redirect(url_for("drive"))
    else:
        folders = db.execute("SELECT * FROM folders WHERE user_id = ?", session["user_id"])
        folder_tree = build_folder_tree(folders)
        return render_template("createFolder.html", folder_tree=folder_tree)


@app.route("/Cfile", methods=["GET", "POST"])
@login_required
def Cfile():
    if request.method == "POST":
        file = request.files["file"]
        folder_id = request.form.get("folder_id") or None
        user_id = session["user_id"]

        if not file or file.filename == "":
            return "Archivo no válido", 400

        filename = secure_filename(file.filename)

        # Ruta base del usuario
        user_root = os.path.join(app.config["UPLOAD_FOLDER"], str(user_id))

        # Si hay carpeta lógica, construir ruta física
        if folder_id:
            folder_path = os.path.join(user_root, build_folder_path(int(folder_id)))
        else:
            folder_path = user_root

        os.makedirs(folder_path, exist_ok=True)

        file_path = os.path.join(folder_path, filename)
        file.save(file_path)

        # Guardar en la base de datos
        db.execute(
            "INSERT INTO files (filename, filepath, folder_id, user_id) VALUES (?, ?, ?, ?)",
            filename, file_path, folder_id, user_id
        )
        flash("File uploaded successfully!! :] ")
        return redirect("/drive")

    else:
        folders = db.execute("SELECT * FROM folders WHERE user_id = ?", session["user_id"])
        folder_tree = build_folder_tree(folders)
        return render_template("createFile.html", folder_tree=folder_tree)





@app.route("/create_file", methods=["POST"])
@login_required
def create_file():

    #  Obtener datos del formulario
    raw_name = request.form["filename"].strip()
    content = request.form["content"]
    selected_mode = request.form.get("mode") or "plain_text"
    folder_id = request.form.get("folder_id") or None
    user_id = session["user_id"]

    #  Si el nombre no tiene extensión, usar por defecto .txt
    if "." in raw_name:
        filename = secure_filename(raw_name)
    else:
        # Inferir la extensión desde el modo seleccionado
        extension_map = {
            "python": "py", "javascript": "js", "htmlmixed": "html", "css": "css",
            "text/x-java": "java", "text/x-csrc": "c", "text/x-c++src": "cpp", "text/x-csharp": "cs",
            "php": "php", "ruby": "rb", "go": "go", "rust": "rs", "markdown": "md",
            "sql": "sql", "shell": "sh", "xml": "xml", "yaml": "yml", "json": "json",
            "stex": "tex", "perl": "pl", "lua": "lua", "swift": "swift", "scala": "scala",
            "kotlin": "kt", "dart": "dart", "haskell": "hs", "clojure": "clj", "elixir": "ex",
            "erlang": "erl", "pascal": "pas", "vb": "vb", "verilog": "v", "vhdl": "vhd",
            "nginx": "conf", "dockerfile": "Dockerfile", "protobuf": "proto", "tcl": "tcl",
            "twig": "twig", "pug": "pug", "handlebars": "hbs", "sass": "sass",
            "scss": "scss", "less": "less"
        }

        extension = extension_map.get(selected_mode, "txt")
        filename = secure_filename(raw_name) + "." + extension

    #  Crear la ruta de guardado
    user_root = os.path.join(app.config["UPLOAD_FOLDER"], str(user_id))
    if folder_id:
        folder_path = os.path.join(user_root, build_folder_path(int(folder_id)))
    else:
        folder_path = user_root
    os.makedirs(folder_path, exist_ok=True)

    file_path = os.path.join(folder_path, filename)

    #  Escribir el contenido
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
    except Exception as e:
        return apology(f"Error al guardar archivo: {e}", 500)

    #  Registrar en la base de datos
    db.execute(
        "INSERT INTO files (filename, filepath, folder_id, user_id) VALUES (?, ?, ?, ?)",
        filename, file_path, folder_id, user_id
    )

    flash("File created successfully!! :] ")
    return redirect("/drive")





@app.route("/drive")
@login_required
def drive():
    files = db.execute("SELECT * FROM files WHERE user_id = ?", session["user_id"])
    folders = db.execute("SELECT * FROM folders WHERE user_id = ?", session["user_id"])
    folder_ = archi(folders, files)
    folder_tree = folder_["folders"]
    files = folder_["files"]
    return render_template("drive.html", folder_tree=folder_tree, files=files)




@app.route("/shares")
@login_required
def shares():
    compartidosIn = {"folders": [], "files": []}
    user_id = session["user_id"]

    # 1) Permisos de carpetas compartidas
    sharedFolders = db.execute(
        "SELECT * FROM permissions WHERE user_id = ? AND folder_id IS NOT NULL",
        user_id
    )
    for perm in sharedFolders:
        root_id = perm["folder_id"]
        allF, allFi = hacerCarpeta(root_id)            # recursión plana
        tree = archi2(allF, allFi, root_id)             # nueva versión

        # añadir metadatos de quién y nivel de acceso
        j = db.execute("SELECT username FROM users WHERE id = ?", perm["puser_id"])
        if j:
            tree["shared_by"] = j[0]["username"]
            tree["access"]    = perm["access_level"]
            compartidosIn["folders"].append(tree)


    # Permisos de archivos sueltos
    sharedFiles = db.execute(
        "SELECT * FROM permissions WHERE user_id = ? AND file_id IS NOT NULL",
        user_id
    )
    for perm in sharedFiles:
        f = db.execute("SELECT * FROM files WHERE id = ?", perm["file_id"])
        if not f:
            continue #se salta si no hay archivo
        f = f[0]
        j = db.execute("SELECT username FROM users WHERE id = ?", perm["puser_id"])
        if j:
            f["shared_by"] = j[0]["username"]
            f["access"]    = perm["access_level"]
            compartidosIn["files"].append(f)


    # parte de los compartidos del usuario
    compartidosOut = {"folders": [], "files": []}

    # carpetas que ha compartido el usuario
    foldersOut = db.execute(
        "SELECT * FROM permissions WHERE puser_id = ? AND folder_id IS NOT NULL",
        user_id
    )
    # evitar duplicados -----------------------------------------------------------
    if foldersOut:
        folderO = {}
        fols = []
        ids = []
        for folder in foldersOut:

            if folder["folder_id"] not in ids:
                ids.append(folder["folder_id"])
                fols.append(folder)
            folderO[folder["folder_id"]] = []
            folderO[folder["folder_id"]].append(folder["user_id"])


        for perm in fols:
            root_id = perm["folder_id"]
            allF, allFi = hacerCarpeta(root_id)            # recursión plana
            tree = archi2(allF, allFi, root_id)             # nueva versión

            nuevosID = []
            shared_username = {}
            # añadir metadatos de quién y nivel de acceso
            if perm["folder_id"] in folderO:
                nuevosID = folderO[perm["folder_id"]]

            for uid in nuevosID:
                j = db.execute("SELECT username FROM users WHERE id = ?", uid)
                if j:
                    shared_username[j[0]["username"]] = db.execute("SELECT access_level FROM permissions WHERE user_id = ? AND folder_id = ?", uid, perm["folder_id"])[0]["access_level"]

            j = db.execute("SELECT username FROM users WHERE id = ?", perm["user_id"])
            if j:

                shared_username[j[0]["username"]] = perm["access_level"]
                tree["shared_for"] = shared_username
                compartidosOut["folders"].append(tree)


     # Permisos de archivos sueltos
     #----------------------------------------------------------------------------------------
    filesOut = db.execute(
        "SELECT * FROM permissions WHERE puser_id = ? AND file_id IS NOT NULL",
        user_id )

    if filesOut:
        filesO = {}
        fils = []
        ides = []

        for file in filesOut:
            if file["file_id"] not in ides:
                ides.append(file["file_id"])
                fils.append(file)
            filesO[file["file_id"]] = []
            filesO[file["file_id"]].append(file["user_id"])


        for perm in fils:
            f = db.execute("SELECT * FROM files WHERE id = ?", perm["file_id"])
            if not f:
                continue #se salta si no hay archivo
            f = f[0]

            fnuevosID = []
            fshared_username = {}
            # añadir metadatos de quién y nivel de acceso
            if perm["file_id"] in filesO:
                fnuevosID = filesO[perm["file_id"]]

            for uid in fnuevosID:
                j = db.execute("SELECT username FROM users WHERE id = ?", uid)
                if j:
                    fshared_username[j[0]["username"]] = db.execute("SELECT access_level FROM permissions WHERE user_id = ? AND file_id = ?", uid, perm["file_id"])[0]["access_level"]


            j = db.execute("SELECT username FROM users WHERE id = ?", perm["user_id"])
            if j:

                fshared_username[j[0]["username"]] = perm["access_level"]
                f["shared_for"] = fshared_username
                compartidosOut["files"].append(f)



    return render_template("shares.html",
        folders = compartidosIn["folders"],
        files = compartidosIn["files"],
        userFolders = compartidosOut["folders"],
        userFiles = compartidosOut["files"]
    )


# prototipado
@app.route("/shares2")
@login_required
def share4s():
    compWh = {}
    compWh["folders"] = []
    compWh["files"] = []

    user_id = session["user_id"]
    wfiles = db.execute("SELECT * FROM permissions WHERE user_id = ? AND file_id IS NOT NULL", user_id)
    wfolders = db.execute("SELECT * FROM permissions WHERE user_id = ? AND folder_id IS NOT NULL", user_id)

    if wfolders:
        for folder in wfolders:
            fol = hacerCarpeta(folder["folder_id"])
            folder_ = archi(fol[0], fol[1])

            jef = db.execute("SELECT username FROM users WHERE id = ?", folder["puser_id"])
            if jef:
                folder_["shared_by"] = jef[0]["username"]
                folder_["access"] = folder["access_level"]

                compWh["folders"].append(folder_)

    if wfiles:
        for file in wfiles:
            file_ = db.execute("SELECT * FROM files WHERE id = ?", file["file_id"])
            if file_:
                jef = db.execute("SELECT username FROM users WHERE id = ?", file["puser_id"])
                if jef:
                    file_[0]["shared_by"] = jef[0]["username"]
                    file_[0]["access"] = file["access_level"]
                    compWh["files"].append(file_[0])

    folders = compWh["folders"]
    files = compWh["files"]
    return render_template("shares.html", folders=folders, files=files)




@app.route("/profile")
@login_required
def profile():
    user_id = session["user_id"]
    count = [0, 0, 0, 0, 0, 0]
    key = "None"

    keyDB = db.execute("SELECT key FROM keys WHERE user_id = ?", user_id)
    if keyDB:
        key = keyDB[0]["key"]

    cursor = db.execute("SELECT COUNT(*) FROM files WHERE user_id = ?", user_id)
    if cursor:
        count.insert(0, cursor[0]["COUNT(*)"])

    cursor = db.execute("SELECT COUNT(*) FROM folders WHERE user_id = ?", user_id)
    if cursor:
        count.insert(1, cursor[0]["COUNT(*)"])

    cursor = db.execute("SELECT COUNT(*) FROM permissions WHERE puser_id = ? AND file_id IS NOT NULL", user_id)
    if cursor:
        count.insert(2, cursor[0]["COUNT(*)"])

    cursor = db.execute("SELECT COUNT(*) FROM permissions WHERE puser_id = ? AND folder_id IS NOT NULL", user_id)
    if cursor:
        count.insert(3, cursor[0]["COUNT(*)"])

    cursor = db.execute("SELECT COUNT(*) FROM permissions WHERE user_id = ? AND file_id IS NOT NULL", user_id)
    if cursor:
        count.insert(4, cursor[0]["COUNT(*)"])

    cursor = db.execute("SELECT COUNT(*) FROM permissions WHERE user_id = ? AND folder_id IS NOT NULL", user_id)
    if cursor:
        count.insert(5, cursor[0]["COUNT(*)"])

    cursor = db.execute("SELECT * FROM users WHERE id = ?", user_id)

    return render_template("profile.html",
                           files=count[0],
                           folders=count[1],
                           shared_files=count[2],
                           shared_folders=count[3],
                           shared_files_you=count[4],
                           shared_folders_you=count[5],
                           name=cursor[0]["username"],
                           id=cursor[0]["id"],
                           key=key
                           )

@app.route("/specialKey")
@login_required
def llave():
    user_id = session["user_id"]
    key = simpleHash(user_id, None)

    comprobar = db.execute("SELECT * FROM keys WHERE user_id = ?", user_id)
    if not comprobar:
        db.execute("INSERT INTO keys (user_id, key) VALUES (?, ?)", user_id, key)
        flash("Generated special Key!! ___ It's unique per user, don't share it ________  ദ്ദി(ᵔᗜᵔ) ")
        return redirect("/profile")
    flash("You already have a key ( -_•)")
    return redirect("/profile")



# llaves -------------------------------------------------------------------------------------------------

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


@app.route("/deleteSpecialKey")
@login_required
def deleteKey():
    user_id = session["user_id"]
    key = db.execute("SELECT * FROM keys WHERE user_id = ?", user_id)
    if key:
        db.execute("DELETE FROM keys WHERE user_id = ?", user_id)
        flash("Delete successfully ദ്ദി(ᵔᗜᵔ)")
        return redirect("/profile")
    flash("You do not have a key!! ( -_•)")
    return redirect("/profile")

#---------------------------------------------------------------------------------------------------------
# Ajustes de shares.html

@app.route("/changeAccess/<int:folder_id>/<c>", methods=["POST"])
@login_required
def changeAccess(folder_id, c):
    ID = db.execute("SELECT id FROM users WHERE username = ?", c)[0]["id"]
    accessLevel = request.form.get("level")
    if not accessLevel:
        flash("MISSING Access Level ( -_•)")
        return redirect("/shares")

    user_id = session["user_id"]

    db.execute(
        "UPDATE permissions SET access_level = ? WHERE folder_id = ? AND user_id = ? AND puser_id = ?",
        accessLevel, folder_id, ID, user_id
          )
    flash("Access level changed successfully  ദ്ദി(ᵔᗜᵔ) ")
    return redirect("/shares")


@app.route("/remove/<int:folder_id>/<c>")
@login_required
def removeShared(folder_id, c):
    ID = db.execute("SELECT id FROM users WHERE username = ?", c)[0]["id"]
    user_id = session["user_id"]
    db.execute("DELETE FROM permissions WHERE folder_id = ? AND user_id = ? AND puser_id = ?", folder_id, ID, user_id)
    flash("Remove permission successfully ദ്ദി(ᵔᗜᵔ)")
    return redirect("/shares")



# --------------------------------------------------------------------------------------

@app.route("/changeAccessf/<int:file_id>/<c>", methods=["POST"])
@login_required
def changeAccessFile(file_id, c):
    ID = db.execute("SELECT id FROM users WHERE username = ?", c)[0]["id"]
    accessLevel = request.form.get("level")
    if not accessLevel:
        flash("MISSING Access Level ( -_•)")
        return redirect("/shares")

    user_id = session["user_id"]

    db.execute(
        "UPDATE permissions SET access_level = ? WHERE file_id = ? AND user_id = ? AND puser_id = ?",
        accessLevel, file_id, ID, user_id
          )
    flash("Access level changed successfully  ദ്ദി(ᵔᗜᵔ) ")
    return redirect("/shares")


@app.route("/removef/<int:file_id>/<c>")
@login_required
def removeSharedFile(file_id, c):
    ID = db.execute("SELECT id FROM users WHERE username = ?", c)[0]["id"]
    user_id = session["user_id"]

    db.execute("DELETE FROM permissions WHERE file_id = ? AND user_id = ? AND puser_id = ?", file_id, ID, user_id)
    flash("Remove permission successfully ദ്ദി(ᵔᗜᵔ)")
    return redirect("/shares")

#---------------------------------------------------------------------------------------------------------------


# parte de ajustes adicionales por archivo o carpeta
# ----------------------------------------------------------------------------------------------------------------





@app.route("/delete_folder/<int:folder_id>", methods=["GET", "POST"])
@login_required
def delete_folder(folder_id):
    # borrar carpeta y su contenido
    # extrae el folder
    folder = db.execute("SELECT * FROM folders WHERE id = ?", folder_id)
    if not folder:
        flash("Folder doesn’t exist 🗃️")
        return redirect("/drive")

    # se verifica el user_id
    user_id = session["user_id"]
    if folder[0]["user_id"] != user_id:
        flash("Access denied ")
        return redirect("/drive")

    # se arma la ruta absoluta del folder
    folder_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        str(user_id),
        build_folder_path(folder_id)
    )

    # si esta fisicamente existe
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
        # diferencia entre usar shutil.smtree y os.remove, es que uno esta directamente pensado para archivos
        # mientras que shutil elimina todas las sub carpetas y archivos dentro de esta ruta folder_path

    # Limpieza en base de datos
    db.execute("DELETE FROM permissions WHERE folder_id = ?", folder_id)
    db.execute("DELETE FROM files WHERE folder_id = ?", folder_id)

    db.execute("DELETE FROM folders WHERE parent_id = ?", folder_id)
    db.execute("DELETE FROM folders WHERE id = ?", folder_id)

    flash("Folder deleted successfully!! :)")
    return redirect("/drive")



@app.route("/share_folder/<int:folder_id>", methods=["GET", "POST"])
@login_required
def share_folder(folder_id):
    # compartir carpeta por id
    if request.method == "POST":
        idperson = request.form.get("user_id").strip()
        accessLevel = request.form.get("level")

        if not idperson:
            return apology("MISSING ID", 400)
        if not accessLevel:
            return apology("MISSING ACCESS", 400)

        id = db.execute("SELECT id FROM users WHERE id = ?", idperson)
        if not id:
            return apology("USER DOES NOT EXIST", 404)

        idd = id[0]["id"]
        preca = db.execute("SELECT user_id, folder_id FROM permissions WHERE user_id = ? AND folder_id = ?", idd, folder_id)

        if not preca:
            user = session["user_id"]


            db.execute("INSERT INTO permissions (user_id, folder_id, access_level, puser_id) VALUES (?, ?, ?, ?)", idd, folder_id, accessLevel, user)
            db.execute("UPDATE folders SET is_private = 0 WHERE id = ?", folder_id)
            flash("Folder shared successfully!!")
            return redirect("/drive")
        return apology("THE USER ALREADY HAS PERMISSION", 400)
    else:
        pass





@app.route("/rename_folder/<int:folder_id>", methods=["GET", "POST"])
@login_required
def rename_folder(folder_id):
    # renombrar carpeta
    newName = request.form.get("newName").strip()
    if not newName:
        return apology("MISSING NAME", 400)
    newName = secure_filename(newName)
    if len(newName) > 100:
        flash("That name is too long (╥_╥)")
        return redirect("/drive")

    # se saca el folder de la base de datos
    folder = db.execute("SELECT * FROM folders WHERE id = ?", folder_id)
    if not folder:
        flash("The folder do not exist :/")
        return redirect("/drive")

    if folder[0]["name"] == newName:
        flash("The name is already set to that.")
        return redirect("/drive")

    if folder[0]["parent_id"] == None:
        carpetasRaiz = db.execute("SELECT * FROM folders WHERE parent_id IS NULL")
        for carpeta in carpetasRaiz:
            if carpeta["name"] == newName:
                flash("Another file already has exactly this name ( -_•)")
                return redirect("/drive")


    # se extrae su carpeta madre
    carpetaMadre = db.execute("SELECT * FROM folders WHERE parent_id = ?", folder[0]["parent_id"])
    if carpetaMadre:
        # se asegura de que el nombre no se repita
        for carpeta in carpetaMadre:
            if carpeta["name"] == newName:
                flash("Another file already has exactly this name ( -_•)")
                return redirect("/drive")

     # se asegura que el usuario si sea el propietario
    user_id = session["user_id"]
    if folder[0]["user_id"] == user_id:
        pathFolder = build_folder_path(folder[0]["parent_id"])
        # se escriben las dos rutas absolutas
        path = os.path.join(app.config["UPLOAD_FOLDER"], str(user_id), pathFolder, folder[0]["name"])
        Newpath = os.path.join(app.config["UPLOAD_FOLDER"], str(user_id), pathFolder, newName)

        # se renombra el archivo
        os.rename(path, Newpath)

        # ultimos ajustes en la base de datos
        db.execute("UPDATE folders SET name = ? WHERE id = ?", newName, folder_id)
        flash("Foldername changed successfully ദ്ദി(ᵔᗜᵔ)")
        return redirect("/drive")

    flash("action invalid (╯°□°）╯︵ ┻━┻")
    return redirect("/drive")








@app.route("/rename_file/<int:file_id>", methods=["POST"])
@login_required
def renameFile(file_id):
    # se extrae el nombre
    newName = request.form.get("newName").strip()
    if not newName:
        return apology("MISSING NAME", 400)
    #se pasa por filtro de seguridad
    newName = secure_filename(newName)

    # controla un flujo innecesario
    if len(newName) > 100:
        flash("That name is too long (╥_╥)")
        return redirect("/drive")

    # se saca el file de la base de datos
    file = db.execute("SELECT * FROM files WHERE id = ?", file_id)
    if not file:
        flash("The file do not exist :/")
        return redirect("/drive")

    if file[0]["filename"] == newName:
        flash("The name is already set to that.")
        return redirect("/drive")

    if file[0]["folder_id"] == None:
        carpetasRaiz = db.execute("SELECT * FROM files WHERE folder_id IS NULL")
        for carpeta in carpetasRaiz:
            if carpeta["filename"] == newName:
                flash("Another file already has exactly this name ( -_•)")
                return redirect("/drive")


    # se extrae su carpeta madre
    carpetaMadre = db.execute("SELECT * FROM files WHERE folder_id = ?", file[0]["folder_id"])
    if carpetaMadre:
        # se asegura de que el nombre no se repita
        for archivo in carpetaMadre:
            if archivo["filename"] == newName:
                flash("Another file already has exactly this name ( -_•)")
                return redirect("/drive")

    # se asegura que el usuario si sea el propietario
    user_id = session["user_id"]
    if file[0]["user_id"] == user_id:
        pathFile = build_folder_path(file[0]["folder_id"])
        # se escriben las dos rutas absolutas
        path = os.path.join(app.config["UPLOAD_FOLDER"], str(user_id), pathFile, file[0]["filename"])
        Newpath = os.path.join(app.config["UPLOAD_FOLDER"], str(user_id), pathFile, newName)

        # se renombra el archivo
        os.rename(path, Newpath)

        # ultimos ajustes en la base de datos
        db.execute("UPDATE files SET filename = ? WHERE id = ?", newName, file_id)
        flash("Filename changed successfully ദ്ദി(ᵔᗜᵔ)")
        return redirect("/drive")

    flash("action invalid (╯°□°）╯︵ ┻━┻")
    return redirect("/drive")




@app.route("/delete_file/<int:file_id>", methods=["GET", "POST"])
@login_required
def delete_file(file_id):
    # borrar archivo
    file = db.execute("SELECT * FROM files WHERE id = ?", file_id)
    if not file:
        flash("The file do not exist :/")
        return redirect("/drive")

    user_id = session["user_id"]
    if file[0]["user_id"] != user_id:
        flash("Action denied (¬_¬)")
        return redirect("/drive")

    file_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        str(user_id),
        build_file_path(file_id)
    )

    if os.path.exists(file_path):
        os.remove(file_path)


    db.execute("DELETE FROM permissions WHERE file_id = ?", file_id)
    db.execute("DELETE FROM files WHERE id = ?", file_id)
    flash("File deleted successfully!! :)")
    return redirect("/drive")




@app.route("/share_file/<int:file_id>", methods=["GET", "POST"])
@login_required
def share_file(file_id):
    # compartir archivos por id
    if request.method == "POST":
        idperson = request.form.get("user_id").strip()
        accessLevel = request.form.get("level")

        if not idperson:
            return apology("MISSING ID", 400)
        if not accessLevel:
            return apology("MISSING ACCESS", 400)

        id = db.execute("SELECT id FROM users WHERE id = ?", idperson)
        if not id:
            return apology("USER DOES NOT EXIST", 404)
        id_ = id[0]["id"]


        preca = db.execute("SELECT * FROM permissions WHERE user_id = ? AND file_id = ?", id_, file_id)
        if not preca:
            user = session["user_id"]


            db.execute("INSERT INTO permissions (user_id, file_id, access_level, puser_id) VALUES (?, ?, ?, ?)", id_, file_id, accessLevel, user)
            db.execute("UPDATE files SET is_private = 0 WHERE id = ?", file_id)
            flash("File shared successfully!!")
            return redirect("/drive")
        return apology("THE USER ALREADY HAS PERMISSION", 400)
    else:
        pass
















@app.route("/download_file/<int:file_id>")
@login_required
def download_file(file_id):
    # Se obtiene la ruta absoluta del archivo
    puser_id = db.execute("SELECT * FROM files WHERE id = ?", file_id)[0]["user_id"]
    path = os.path.join(app.config["UPLOAD_FOLDER"], str(puser_id), build_file_path(str(file_id)))

    # se retorna el archivo en la ruta path con as_attachment para que descargue
    return send_file(path, as_attachment=True)



@app.route("/download_folder/<int:folder_id>")
@login_required
def download_folder(folder_id):
    # usuario y rutas del folder
    puser_id = db.execute("SELECT * FROM folders WHERE id = ?", folder_id)[0]
    subpath = build_folder_path(str(folder_id))
    if not subpath:
        return apology("FOLDER NOT FOUND", 404)

    # arma la ruta absoluta en la que se encuentra la carpeta
    path = os.path.join(app.config["UPLOAD_FOLDER"], str(puser_id["user_id"]), subpath)


    # crea una ruta dinamica temporal donde guardar el zip
    # dentro de la carpeta temporal se ve como /tmp/nombreFolder.zip
    temp_dir = tempfile.mkdtemp() # crea un dierctorio temporal como en /tmp
    zip_path = os.path.join(temp_dir, f"{puser_id['name']}.zip") # se une al nombre del folder


    # Se abre archivo y se comprime recorriendo todas sus subcarpetas y archivos
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(path):

            for dir_ in dirs:
                rutaAbsoluta = os.path.join(root, dir_)
                rutaRelativa = os.path.relpath(rutaAbsoluta, path) + "/"
                #crea carpeta si es que esta vacia
                zipf.writestr(rutaRelativa, "") # writestr() agrega al zip contenido dinamico, no necesariamente
                # archivos fisicos, aca el a cada ruta o entrada vacia (carpetas sin contenido)


            for file in files:
                full_path = os.path.join(root, file) # ruta absoluta de la carpeta (solo importa el interior)
                arcname = os.path.relpath(full_path, path) # esta parte genera el nombre vitual o independiente del archivo
                # si path = /uploads/proyecto
                # y full_path = /uploads/proyecto/docs/manual.txt
                # arcname = docs/manual.txt
                # esto indica que la carpeta compartida es /proyecto
                zipf.write(full_path, arcname) # introduce el archivo /// le da nombre virtual
                # write() si se usa para archivos fisicos donde se da su ruta y el nombre

    # as_attachment=True indica que se descargue
    response = send_file(zip_path, as_attachment=True) # envia archivo como respuesta al servidor

    # antes de que se cierre la solicitud y despues de enviar respuesta al cliente
    @response.call_on_close
    def clear():
        shutil.rmtree(temp_dir) # elimina el archivo temporal

    # retorna el archivo .zip
    return response


#with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:  es la forma en la que se abre y se
        # crea un .zip, el ZIP_DEFLATED indica la forma de compresion
#------------------------------------------------------------------------------------------------
        # la funcion walk recorre cada subcarpeta y archivo en forma de arbol por ejemplo:
"""         for root, dirs, files in os.walk("uploads/project"):
            print("📁", root)
            print("  ➤ Subcarpetas:", dirs)
            print("  ➤ Archivos:", files)


            📁 uploads/project
                ➤ Subcarpetas: ['images']
                ➤ Archivos: ['report.txt']

            📁 uploads/project/images
                ➤ Subcarpetas: []
                ➤ Archivos: ['photo1.jpg', 'photo2.jpg'] """
#------------------------------------------------------------------------------------------





# --------------------------------------------------------------------------------------------------------------


@app.route("/file_ep/<int:file_id>/<i>", methods=["GET", "POST"])
@login_required
def file_ep(file_id, i):
    # toma el archivo
    file = db.execute("SELECT * FROM files WHERE id = ?", file_id)
    if not file:
        return apology("Error not found file", 404)

    puser_id = file[0]["user_id"]
    user_id = session["user_id"]

    # arma una ruta absoluta
    pathFile = os.path.join(app.config["UPLOAD_FOLDER"], str(puser_id), build_file_path(str(file_id)))

    if not os.path.exists(pathFile):
        return apology("File not found on server", 404)

    # guarda el contenido del achivo
    try:
        with open(pathFile, 'r', encoding='utf-8') as f:
            file_content = f.read()
    except Exception as e:
        file_content = f"# Error reading file: {str(e)}"

    # mode_ significa la extension del archivo por ejemplo .py
    mode_ = mode(file[0]["filename"])

    # se extrae informacion del usuario para ver su nivel de acceso
    user = db.execute("SELECT * FROM users WHERE id = ?", user_id)
    if user:
        user = user[0]
        if i != "owner":
            nivel = i
            if nivel == "editor":
                nivel = "editing"
            elif nivel == "reader":
                nivel = "viewing"

        # si no esta en la tabla pero su id es el mismo que el user_id del archivo
        else:
            if file[0]["user_id"] == user_id:
                nivel = "editing" #owner
    # se envial los datos relevantes
    flash("____File name: " + file[0]["filename"] + "____­­­­­­­­­­­­­­­­­")

    return render_template('editFile.html', file=file,
                                            content=file_content,
                                            mode_=mode_,
                                            user=user,
                                            level=nivel,
                                            modo=i)


@app.route("/autosave/<int:file_id>", methods=["POST"])
@login_required
def autosave(file_id):
    content = request.get_json().get("content", "")
    file = db.execute("SELECT * FROM files WHERE id = ?", file_id)
    pathFile = os.path.join(app.config["UPLOAD_FOLDER"], str(file[0]["user_id"]), build_file_path(str(file_id)))

    try:
        with open(pathFile, "w", encoding="utf-8") as f:
            f.write(content)
        return jsonify({"status": "saved"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


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

#-------------------------------------------------------------------------

@app.route("/read_file/<int:file_id>")
@login_required
def readFile(file_id):
    user_id = session["user_id"]
    file = db.execute("SELECT * FROM files WHERE id = ?", file_id)
    if file:
        if user_id == file[0]["user_id"]:
            return redirect(url_for('file_ep', file_id=file_id, i="owner"))
        permiso = db.execute("SELECT * FROM permissions WHERE user_id = ? AND file_id = ? AND access_level = 'reader'",
                            user_id, file_id)
        if permiso:
            return redirect(url_for('file_ep', file_id=file_id, i="reader"))

        permisoAlternativo = hayPermiso(file, user_id)
        if permisoAlternativo:
            return redirect(url_for('file_ep', file_id=file_id, i="reader"))
        return apology("You don't have PERMISSION", 400)
    return apology("FILE DOES NOT EXIST", 404 )



@app.route("/edit_file/<int:file_id>")
@login_required
def editFile(file_id):
    user_id = session["user_id"]
    file = db.execute("SELECT * FROM files WHERE id = ?", file_id)
    if file:
        if user_id == file[0]["user_id"]:
            return redirect(url_for('file_ep', file_id=file_id, i="owner"))
        permiso = db.execute("SELECT * FROM permissions WHERE user_id = ? AND file_id = ? AND access_level = 'editor'",
                              user_id, file_id)
        if permiso:
            return redirect(url_for('file_ep', file_id=file_id, i="editor"))

        permisoAlternativo = hayPermiso(file, user_id)
        if permisoAlternativo:
            return redirect(url_for('file_ep', file_id=file_id, i="editor"))
        return apology("You don't have PERMISSION", 400)
    return apology("FILE DOES NOT EXIST", 404 )
# redirect va al metodo
#-------------------------------------------------------------------------------


@app.route("/veri", methods=["POST"])
def verificar_():
    session.clear()

    data = request.json
    username = data.get("user").strip()
    password = data.get("password").strip()

    user = db.execute("SELECT * FROM users WHERE username = ?", username)
    if not user:
        return jsonify({"resultado": 3})

    if check_password_hash(user[0]["hash"], password):
        session["user_id"] = user[0]["id"]
        return jsonify({"resultado": 1})
    else:
        return jsonify({"resultado": 3})



@app.route("/llave_", methods=["POST"])
def llavev():
    data = request.get_json()
    key = data.get("valor", "").strip()

    # Buscar el user_id relacionado con la key
    rows = db.execute("SELECT user_id FROM keys WHERE key = ?", key)
    if rows:
        user_id = rows[0]["user_id"]

        # Buscar al usuario en base al user_id
        user = db.execute("SELECT * FROM users WHERE id = ?", user_id)
        if user:
            session["user_id"] = user[0]["id"]
            return jsonify({
                "resultado": 1,
                "name": user[0]["username"]
            })

    # Si no se encontró key o usuario
    return jsonify({"resultado": 0})




#API Para archivos
#---------------------------------------------------------------------------------

@app.route("/subir", methods=["POST"])
def subir():
    if 'archivo' not in request.files:
        return jsonify({"error": "No file was sent ( ˘︹˘ )"}), 400

    archivo = request.files['archivo']
    folder_id = request.form.get("folderid").strip()

    if archivo.filename == "":
        return jsonify({"error": "Empty file name ( ˘︹˘ )"}), 400

    user_id = session["user_id"]
    path = os.path.join(app.config["UPLOAD_FOLDER"], str(user_id))

    if folder_id != "z":
        isEntero = es_entero(folder_id)
        if isEntero:
            folder = db.execute("SELECT * FROM folders WHERE id = ?", folder_id)
            if folder:
                rutaRelativa = build_folder_path(folder_id)
                rutaAbsoluta = os.path.join(path, rutaRelativa, archivo.filename)

                os.makedirs(os.path.dirname(rutaAbsoluta), exist_ok=True)
                archivo.save(rutaAbsoluta)

                #  Registrar en la base de datos
                db.execute(
                    "INSERT INTO files (filename, filepath, folder_id, user_id) VALUES (?, ?, ?, ?)",
                    archivo.filename, rutaAbsoluta, folder_id, user_id
                )

                return jsonify({"mensaje": f"The File: '{archivo.filename}' Uploaded successfully (>‿◠)✌ in '{folder[0]["name"]}'!"}), 200
            return jsonify({"error": "Folder does not exist ( ˘︹˘ )"}), 400
        return jsonify({"error": "Invalid folderID ( ˘︹˘ )"}), 400

    elif folder_id == "z":
        rutaAbsoluta = os.path.join(path, archivo.filename)

        os.makedirs(os.path.dirname(rutaAbsoluta), exist_ok=True)
        archivo.save(rutaAbsoluta)

        #  Registrar en la base de datos
        db.execute(
            "INSERT INTO files (filename, filepath, folder_id, user_id) VALUES (?, ?, ?, ?)",
            archivo.filename, rutaAbsoluta, None, user_id
        )
        session.clear()
        return jsonify({"mensaje": f"The File: '{archivo.filename}' Uploaded successfully (>‿◠)✌ in your Root!"})


# para subir a carpeta especifica
@app.route("/fol", methods=["POST"])
def folder():
    user_id = session["user_id"]
    data = request.json
    folder_id = data.get("folderid").strip()

    if es_entero(folder_id):
        folder = db.execute("SELECT * FROM folders WHERE id = ?", folder_id)
        if folder:
            id_ = folder[0]["user_id"]
            if id_ == user_id:
                return jsonify({"respuesta": 0})
            else:
                permiso = db.execute("""SELECT * FROM permissions WHERE
                                     user_id = ?
                                     AND puser_id = ?
                                     AND folder_id = ?
                                     AND access_level = 'editor'
                                      """, user_id, folder[0]["user_id"], folder_id)
                if permiso:
                    session["user_id"] = id_
                    return jsonify({"respuesta": 0})
                else:
                    permisoAlternativo = hayPermisoFC(folder_id, user_id, "editor")
                    if permisoAlternativo:
                        session["user_id"] = id_
                        return jsonify({"respuesta": 0})

        return jsonify({"respuesta": 1})
    return jsonify({"respuesta": 1})





#pronto algun endpoint para descargar archivo desde la consola por ID del file o si es posible, igual con folder
# ------------------------------------------------------------------------------------------------------------------
# para descargar archhivo por ID
@app.route("/download_FFC", methods=["POST"])
def downloadFFC():
    data = request.get_json() #recomendado
    file_id = data.get("fileid", "").strip()
    user_id = session["user_id"]

    if user_id == 0:
        puser_id = db.execute("SELECT * FROM files WHERE id = ?", file_id)
        path = os.path.join(app.config["UPLOAD_FOLDER"], str(puser_id[0]["user_id"]), build_file_path(str(file_id)))
        session.clear()
        return send_file(path, as_attachment=True)
    return jsonify({"error": "Invalid file ( ˘︹˘ )"})



# para verificar el archivo a descargar
#------------------------------------------------------------------------------------------------------------------
@app.route("/filename", methods=["POST"])
def name():
    data = request.get_json()
    file_id = data.get("fileid").strip()
    file = db.execute("SELECT * FROM files WHERE id = ?", file_id)
    return jsonify({"respuesta": file[0]["filename"]})


@app.route("/verificar_archivo", methods=["POST"])
def verificarArchivo():
    data = request.get_json()
    file_id = data.get("fileid").strip()
    user_id = session["user_id"]
    permission = None
    file = db.execute("SELECT * FROM files WHERE id = ?", file_id)

    if file:
        id = file[0]["user_id"]
        if user_id == id:
            permission = 1
        else:
            permission = db.execute("""SELECT * FROM permissions WHERE
                                    user_id = ?
                                    AND puser_id = ?
                                    AND file_id = ?
                                    AND access_level = 'editor' """, user_id, id, file_id)
        if permission:
            session["user_id"] = 0
            return jsonify({"respuesta": 0})
        return jsonify({"respuesta": 1})
    return jsonify({"respuesta": 1})

#----------------------------------------------------------------------------------------------------------------
# endpoint para descargar un folder
@app.route("/download_FOFC", methods=["POST"])
def downloadFOFC():
    data = request.get_json()
    folder_id = data.get("folderid").strip()
    user_id = session["user_id"]
    folder = db.execute("SELECT * FROM folders WHERE id = ?", folder_id)

    if folder:
        puser_id = folder[0]["user_id"]

        if user_id == 0:
            # parte que genera el zip
            subpath = build_folder_path(folder_id)
            path = os.path.join(app.config["UPLOAD_FOLDER"], str(puser_id), subpath)

            # directorio temporal
            tmpDir = tempfile.mkdtemp()
            # crea el archivo en la ruta temporal
            pathZip = os.path.join(tmpDir, f"{folder[0]["name"]}.zip")

            with zipfile.ZipFile(pathZip, "w", zipfile.ZIP_DEFLATED) as zipFile:
                for root, dirs, files in os.walk(path):
                    for dir_ in dirs:
                        pathAbsoluta = os.path.join(root, dir_)
                        pathRelativa = os.path.relpath(pathAbsoluta, path) + "/"
                        # si se presenta un ejemplo numerico para lo que esta pasando dentro de relpath
                        # es algo como x1 = 5 y x2 = 7 -> (x2 - x1) = 2 o delta de x

                        zipFile.writestr(pathRelativa, "")

                    for file in files:
                        pathAbsoluta = os.path.join(root, file)
                        pathRelativa = os.path.relpath(pathAbsoluta, path)

                        zipFile.write(pathAbsoluta, pathRelativa)
                        # arg1 = donde se encuentra el archivo
                        #arg2 = dentro del zip ruta donde guardarlo y su nombre final (archivo)
            respuesta = send_file(pathZip, as_attachment=True)

            @respuesta.call_on_close
            def clearFFC():
                shutil.rmtree(tmpDir) # borrar el directorio temporal

            session.clear()
            return respuesta
        return jsonify({"error": "Invalid file ( ˘︹˘ )"}) # sin acceso a la carpeta
    return jsonify({"error": "Invalid file ( ˘︹˘ )"}) # carpeta no existe


@app.route("/foldername", methods=["POST"])
def folname():
    data = request.get_json()
    folder_id = data.get("folderid").strip()
    folder = db.execute("SELECT * FROM folders WHERE id = ?", folder_id)
    return jsonify({"respuesta": folder[0]["name"]})


@app.route("/verificar_carpeta", methods=["POST"])
def verificarCarpeta():
    data = request.get_json()
    folder_id = data.get("folderid").strip()
    user_id = session["user_id"]
    permission = None
    folder = db.execute("SELECT * FROM folders WHERE id = ?", folder_id)

    if folder:
        id = folder[0]["user_id"]
        if user_id == id:
            permission = 1
        else:
            permission = db.execute("""SELECT * FROM permissions WHERE
                                    user_id = ?
                                    AND puser_id = ?
                                    AND folder_id = ?
                                    AND access_level = 'editor' """,
                                    user_id, id, folder_id)
        if permission:
            session["user_id"] = 0
            return jsonify({"respuesta": 0})
        return jsonify({"respuesta": 1})
    return jsonify({"respuesta": 1})






#---------------------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------------------
# para los archivos de consola, se pueden extraer usando
# curl -# -OJ https://silver-barnacle-x55vqwjvgrxpcppp6-5000.app.github.dev/download-sha-down para download

@app.route("/download-sha-down")
def sha_down():
    path = os.path.join(app.root_path, 'static', "shaCodeDOWN.zip")

    try:
        return send_file(
            path,
            as_attachment=True,
            download_name='shaCodeDOWN.zip'
        )
    except FileNotFoundError:
        return "file does not exist :(", 404


@app.route("/download-sha-up")
def sha_up():
    path = os.path.join(app.root_path, 'static', "shaCodeUP.zip")

    try:
        return send_file(
            path,
            as_attachment=True,
            download_name='shaCodeUP.zip'
        )
    except FileNotFoundError:
        return "file does not exist :(", 404

@app.route("/download-sha")
def sha():
    path = os.path.join(app.root_path, 'static', "shaCodeScript.sh")

    try:
        return send_file(
            path,
            as_attachment=True,
            download_name='shaCodeDownloader'
        )
    except FileNotFoundError:
        return "file does not exist :(", 404

#---------------------------------------------------------------------------------
#if __name__ == "__main__":
 #   socketio.run(app, debug=True)



if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5001)
