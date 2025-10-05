#!/bin/bash
# ← Shebang: indica que este script debe ejecutarse usando Bash.

echo "=== Crear Lanzador .desktop ==="
# ← Imprime un título para que el usuario sepa qué está haciendo.

# Pedir al usuario el nombre que tendrá la aplicación en el menú
read -p "Nombre de la aplicación: " app_name

# Pedir la ruta al archivo ejecutable (ej: /home/jhon/Programas/idea/bin/idea.sh)
read -p "Ruta al ejecutable: " exec_path

# Pedir la ruta al icono (.png o .svg)
read -p "Ruta al icono (.png o .svg): " icon_path

# Convertir el nombre a minúsculas y reemplazar espacios con guiones bajos
# Esto se usa para crear el nombre del archivo .desktop sin espacios ni mayúsculas
file_name=$(echo "$app_name" | tr '[:upper:]' '[:lower:]' | tr ' ' '_')
# → tr '[:upper:]' '[:lower:]' convierte mayúsculas en minúsculas
# → tr ' ' '_' reemplaza espacios por guiones bajos

# Definir la ruta completa donde se guardará el archivo .desktop
output="$HOME/.local/share/applications/$file_name.desktop"
# → $HOME es tu carpeta personal (ej: /home/jhon)

# Crear el archivo .desktop usando un bloque de texto (here document)
cat > "$output" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=$app_name
Comment=Lanzador para $app_name
Exec=$exec_path
Icon=$icon_path
Terminal=false
Categories=Utility;
EOF
# → cat > "$output" crea el archivo y escribe dentro lo que hay entre EOF y EOF
# → Las variables como $app_name se expanden automáticamente

# Hacer que el archivo sea ejecutable (necesario para lanzarlo desde entornos gráficos)
chmod +x "$output"

# Confirmar que se creó correctamente
echo " :) Lanzador creado: $output"
