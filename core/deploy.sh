#!/bin/bash
cd ~/iptv
echo "[🚀] Iniciando despliegue a GitHub..."
git add global_jeycamon.m3u jeycamon.json
git commit -m "Auto-Update: $(date +'%Y-%m-%d %H:%M') - Items: $(grep -c '#EXTINF' global_jeycamon.m3u)"
git push
echo "[✔] ¡Proyecto JeycamonTV actualizado en la nube!"
