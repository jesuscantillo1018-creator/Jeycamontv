#!/bin/bash
echo "🚀 Iniciando actualización de Jeycamontv..."

# 1. Ejecutar el script de Python
python pro_list.py

# 2. Preparar los archivos para Git
git add .

# 3. Hacer el commit con la fecha actual
fecha=$(date +'%d-%m-%Y %H:%M')
git commit -m "Actualización automática: $fecha"

# 4. Subir a GitHub
echo "Wait... Subiendo cambios a la nube ☁️"
git push origin maestro

echo "✅ ¡Todo listo! Tu TV ya tiene los canales actualizados."
