#!/bin/bash
# IPs del Grupo Z que encontramos en Shodan
TARGETS=("45.226.168.29" "200.29.48.243" "45.226.171.28" "200.28.0.139")
# Diccionario de rutas donde suelen esconder las películas
PATHS=("vod" "movies" "media" "vids" "hls" "content" "storage" "streaming" "cdn")

echo "🕵️ Iniciando escaneo de directorios VOD en la red Grupo Z..."
echo "----------------------------------------------------------"

for IP in "${TARGETS[@]}"; do
    echo "🔍 Escaneando servidor: $IP"
    for dir in "${PATHS[@]}"; do
        # Probamos la conexión
        STATUS=$(curl -s -o /dev/null -w "%{http_code}" "http://$IP/$dir/")
        
        if [ $STATUS -eq 200 ] || [ $STATUS -eq 301 ]; then
            echo "✅ [ENCONTRADO] -> http://$IP/$dir/ (Status: $STATUS)"
        elif [ $STATUS -eq 403 ]; then
            echo "🔐 [RESTRINGIDO] -> http://$IP/$dir/ (Existe, pero no permite listar)"
        fi
    done
    echo "----------------------------------------------------------"
done

