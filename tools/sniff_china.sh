echo "🎯 AUDITANDO SERVIDOR TENCENT (CHINA): $TARGET_IP"
echo "------------------------------------------------"
urls=(
  "http://$TARGET_IP/vod/"
  "http://$TARGET_IP/iptv-manager/.env"
  "http://$TARGET_IP/iptv-manager/config.php"
  "http://$TARGET_IP/api/v1/streams"
  "http://$TARGET_IP/admin/login.php"
  "http://$TARGET_IP/m3u8"
  "http://$TARGET_IP/hls/"
)

for url in "${urls[@]}"; do
  # Usamos un User-Agent de Android para que el servidor no sospeche
  status=$(curl -I -s -k -A "Dalvik/2.1.0 (Linux; U; Android 13; SM-G998B)" -o /dev/null -w "%{http_code}" "$url")
  echo "[$status] -> $url"
done
