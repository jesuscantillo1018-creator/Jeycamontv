#!/bin/bash
echo "🚀 Iniciando actualización de Jeycamontv..."

# 1. Ejecutar el script interactivo (Aquí es donde te preguntará)
python pro_list.py

# 2. Preparar los cambios para GitHub
git add .

# 3. Crear el mensaje con la fecha actual
fecha=$(date +"%d-%m-%Y %H:%M")
git commit -m "Actualización automática: $fecha"

echo "Wait... Subiendo cambios a la nube ☁️"

# 4. Empujar los cambios (usando rebase para evitar errores de tráfico)
git pull origin maestro --rebase
git push origin maestro

echo "✅ ¡Todo listo! Tu TV ya tiene los canales actualizados."
