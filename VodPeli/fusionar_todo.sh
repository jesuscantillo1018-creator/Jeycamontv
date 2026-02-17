#!/bin/bash

# --- CONFIGURACIÓN DE COLORES ---
VERDE='\033[0;32m'
AZUL='\033[0;34m'
AMARILLO='\033[1;33m'
ROJO='\033[0;31m'
NC='\033[0m'

echo -e "${AZUL}==============================================${NC}"
echo -e "${AZUL}   🚀 MEGA-ACTUALIZADOR JEYCAMON TV V3.0      ${NC}"
echo -e "${AZUL}==============================================${NC}"

# 1. EJECUCIÓN DE RASTREADORES (CAZA DE CONTENIDO)
echo -e "${AMARILLO}📡 Fase 1: Escaneando TV en Vivo por Países...${NC}"
python escanear_vivo.py

echo -e "${AMARILLO}🎬 Fase 2: Clasificando Cine por Géneros...${NC}"
python catalogar_cine.py

echo -e "${AMARILLO}📺 Fase 3: Rastreando Series y Especiales...${NC}"
python catalogar_todo.py

# 2. PROCESO DE FUSIÓN MAESTRA (ORDEN DE PRIORIDAD)
echo -e "${AZUL}⚙️  Fase 4: Unificando y eliminando duplicados...${NC}"

# Creamos un archivo temporal para la mezcla
# El orden aquí define qué aparece primero en la TV del cliente
cat <(echo "#EXTM3U") > temp_unido.m3u

# BLOQUE 1: Canales en Vivo (Países + Deportes)
if [ -f "canales_vivos.m3u" ]; then
    grep -v "#EXTM3U" canales_vivos.m3u >> temp_unido.m3u
fi

# BLOQUE 2: Cine Premium (Ya viene organizado por géneros desde el script)
if [ -f "cine_premium.m3u" ]; then
    grep -v "#EXTM3U" cine_premium.m3u >> temp_unido.m3u
fi

# BLOQUE 3: Series y Anime
if [ -f "series_premium.m3u" ]; then
    grep -v "#EXTM3U" series_premium.m3u >> temp_unido.m3u
fi

# BLOQUE 4: Contenido Extra (Adultos, Novelas, 4K)
if [ -f "extra_premium.m3u" ]; then
    grep -v "#EXTM3U" extra_premium.m3u >> temp_unido.m3u
fi

# BLOQUE 5: Tus Canales Manuales (Base de datos histórica)
if [ -f "../manuales.m3u" ]; then
    grep -v "#EXTM3U" ../manuales.m3u >> temp_unido.m3u
fi

# 3. LIMPIEZA FINAL ANTI-DUPLICADOS (El Filtro Maestro)
# Eliminamos líneas vacías y nos aseguramos que cada URL sea única
grep -v "^$" temp_unido.m3u > temp_limpio.m3u
echo "#EXTM3U" > ../global_jeycamon.m3u
awk '!seen[$0]++' temp_limpio.m3u | grep -v "#EXTM3U" >> ../global_jeycamon.m3u

# Limpiar archivos basura
rm temp_unido.m3u temp_limpio.m3u

# 4. DESPLIEGUE A GITHUB
echo -e "${AMARILLO}📤 Fase 5: Subiendo cambios a GitHub...${NC}"
cd ..
git add .
fecha=$(date +"%d-%m-%Y %H:%M")
git commit -m "🔥 JeycamonTV Ultra Update: TV x Países + Cine Géneros + VOD ($fecha)"
git pull origin maestro --rebase
git push origin maestro

echo -e "${VERDE}==============================================${NC}"
echo -e "${VERDE}   ✅ ¡SISTEMA ACTUALIZADO Y EN LÍNEA!        ${NC}"
echo -e "${VERDE}==============================================${NC}"

