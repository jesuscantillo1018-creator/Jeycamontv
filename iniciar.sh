#!/bin/bash
echo "📦 Verificando dependencias..."
pkg install python -y
pip install flask requests

echo "🔥 Iniciando Panel Xtream Jeycamon en el puerto 8081..."
python ~/iptv/xtream_server.py
