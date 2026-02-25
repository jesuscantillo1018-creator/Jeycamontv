echo "🔍 ESCANEANDO ESTRUCTURA DEL PROYECTO: https://raw.githubusercontent.com/jesuscantillo1018-creator/Jeycamontv/maestro"
urls=(
  "$TARGET_URL/iptv-manager/.env"
  "$TARGET_URL/iptv-manager/config.php"
  "$TARGET_URL/tools/limpiador_ultra.py"
  "$TARGET_URL/global_jeycamon.m3u"
)

for url in "${urls[@]}"; do
  status=$(curl -I -s -k -o /dev/null -w "%{http_code}" "$url")
  echo "[$status] -> $url"
done
