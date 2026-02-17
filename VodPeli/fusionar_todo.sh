#!/bin/bash

# Colores
VERDE='\033[0;32m'
AZUL='\033[0;34m'
NC='\033[0m'

echo -e "${AZUL}🚀 INICIANDO ACTUALIZACIÓN TOTAL JEYCAMON TV...${NC}"

# 1. ESCANEAR TV EN VIVO (PAÍSES)
echo -e "${VERDE}📡 Escaneando señales de TV Latam...${NC}"
python escanear_vivo.py

# 2. RASTREAR VOD (CINE Y SERIES)
echo -e "${VERDE}🎬 Rastreo de Cine, Series y Especiales...${NC}"
python catalogar_cine.py
python catalogar_todo.py

# 3. FUSIÓN MAESTRA CON ORDEN POR PAÍSES
echo "#EXTM3U" > temporal.m3u

# Primero: Tus canales manuales testeados
if [ -f "../manuales.m3u" ]; then
    grep -v "#EXTM3U" ../manuales.m3u >> temporal.m3u
fi

# Segundo: Los canales en vivo que encontró por países
if [ -f "canales_vivos.m3u" ]; then
    grep -v "#EXTM3U" canales_vivos.m3u >> temporal.m3u
fi

# Tercero: Cine y Series
[ -f "cine_premium.m3u" ] && grep -v "#EXTM3U" cine_premium.m3u >> temporal.m3u
[ -f "series_premium.m3u" ] && grep -v "#EXTM3U" series_premium.m3u >> temporal.m3u
[ -f "extra_premium.m3u" ] && grep -v "#EXTM3U" extra_premium.m3u >> temporal.m3u

# Limpieza de duplicados
awk '!seen[$0]++' temporal.m3u > ../global_jeycamon.m3u
rm temporal.m3u

# 4. SUBIDA A GITHUB
cd ..
git add .
git commit -m "🔥 Update: +2600 items + TV Latam por Países + VOD Premium"
git push origin maestro

echo -e "${VERDE}✅ ¡SISTEMA EN LÍNEA! Tus clientes ya tienen los canales por países.${NC}"

