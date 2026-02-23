import requests
import os

def extraer_cine():
    # Fuente de respaldo de alta calidad (VOD Latino/España)
    url = "https://raw.githubusercontent.com/LaneSh442/m3u/main/CINE.m3u"
    output = os.path.expanduser("~/iptv/listas_raw/estrenos_cine.m3u")
    
    print("[🎬] Extrayendo películas de estreno...")
    try:
        r = requests.get(url, timeout=10)
        with open(output, "w", encoding="utf-8") as f:
            f.write(r.text)
        print(f"[✔] ¡ÉXITO! Películas añadidas a listas_raw.")
    except:
        print("[!] Error al conectar con el servidor de cine.")

if __name__ == "__main__":
    extraer_cine()
