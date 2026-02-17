#!/bin/bash
echo "🔥 INICIANDO MEGA-ACTUALIZACIÓN JEYCAMON TV 🔥"

# 1. Ejecutar Rastreadores
echo "🎬 Buscando Películas..."
python catalogar_cine.py

echo "📺 Buscando Series (Interactivo)..."
cd tool_series
python catalogar_series.py
cp series_premium.m3u ../
cd ..

echo "🧬 Buscando Anime, Novelas y Especiales..."
python catalogar_todo.py

# 2. Proceso de Limpieza y Unión
echo "⚙️  Unificando bases de datos..."

# Iniciamos con la base de canales
cat global_jeycamon.m3u > temp.m3u

# Añadimos Cine
if [ -f "cine_premium.m3u" ]; then
    sed '1d' cine_premium.m3u >> temp.m3u
fi

# Añadimos Series
if [ -f "series_premium.m3u" ]; then
    sed '1d' series_premium.m3u >> temp.m3u
fi

# Añadimos Todo lo extra (Anime, Novelas, etc.)
if [ -f "extra_premium.m3u" ]; then
    sed '1d' extra_premium.m3u >> temp.m3u
fi

# Eliminar duplicados y líneas vacías
awk '!seen[$0]++' temp.m3u > global_jeycamon.m3u
rm temp.m3u

# 3. Envío a GitHub
echo "📤 Sincronizando con el servidor GitHub..."
git add .
git commit -m "🚀 Update JeycamonTV: Cine + 315 Series + Anime + Novelas"
git push origin maestro

echo "✅ ¡CATÁLOGO TOTALMENTE ACTUALIZADO!"

