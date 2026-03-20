#!/bin/bash
# Script para iniciar el Servidor IPTV Jeycamon

URL_GITHUB="https://raw.githubusercontent.com/jesuscantillo1018-creator/Jeycamontv/maestro/global_jeycamon.m3u"
PUERTO=8080

echo "🚀 Iniciando Servidor IPTV Jeycamon..."
echo "[🌐] Lista: $URL_GITHUB"
echo "[🔌] Puerto: $PUERTO"

# Verificar si nodejs está instalado
if ! command -v node &> /dev/null; then
    echo "[!] Instalando Node.js..."
    pkg install nodejs-lts -y
fi

# Instalar el proxy si no existe
if ! command -v iptv-proxy &> /dev/null; then
    echo "[!] Instalando iptv-proxy..."
    npm install -g iptv-proxy
fi

# Ejecutar el proxy
iptv-proxy --m3u "$URL_GITHUB" --port $PUERTO
