import xml.etree.ElementTree as ET
import requests

# La URL del servidor que encontraste
url = "http://64.23.147.53:3000/sites/winplay.co/winplay.co.channels.xml"

try:
    response = requests.get(url)
    root = ET.fromstring(response.content)

    print("#EXTM3U")
    for channel in root.findall('channel'):
        name = channel.text
        xml_id = channel.get('xmltv_id')
        site_id = channel.get('site_id')
        
        # Estructura M3U: Metadata + URL (usamos una URL de ejemplo)
        print(f'#EXTINF:-1 tvg-id="{xml_id}" tvg-logo="", {name}')
        print(f'http://servidor-video.com/live/{site_id}.m3u8')

except Exception as e:
    print(f"Error: {e}")
