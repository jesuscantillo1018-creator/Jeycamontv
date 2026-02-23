import requests
import os

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

# Fuentes especializadas por región
fuentes_latam = {
    "COLOMBIA 🇨🇴": ["https://raw.githubusercontent.com/iptv-org/iptv/master/streams/co.m3u"],
    "VENEZUELA 🇻🇪": ["https://raw.githubusercontent.com/iptv-org/iptv/master/streams/ve.m3u"],
    "PERÚ 🇵🇪": ["https://raw.githubusercontent.com/iptv-org/iptv/master/streams/pe.m3u"],
    "CHILE 🇨🇱": ["https://raw.githubusercontent.com/iptv-org/iptv/master/streams/cl.m3u"],
    "CINE PREMIUM 🍿": ["https://raw.githubusercontent.com/Iptv-org-spanish/Peliculas/main/Peliculas.m3u"],
    "DEPORTES ⚽": ["https://raw.githubusercontent.com/LaneSh497/Spanish-IPTV-Lists/main/Deportes.m3u"],
    "ADULTOS 🔥": ["https://raw.githubusercontent.com/Iptv-org-spanish/Adultos/main/Adultos.m3u"]
}

def rastrear():
    raw_path = os.path.expanduser("~/iptv/listas_raw/latam_power.m3u")
    total = 0
    with open(raw_path, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for cat, urls in fuentes_latam.items():
            for url in urls:
                try:
                    r = requests.get(url, headers=headers, timeout=12)
                    if r.status_code == 200:
                        lines = r.text.splitlines()
                        for i in range(len(lines)):
                            if lines[i].startswith("#EXTINF"):
                                info = lines[i]
                                # Forzamos la categoría con bandera
                                if 'group-title' in info:
                                    info = re.sub(r'group-title="[^"]+"', f'group-title="{cat}"', info)
                                else:
                                    info = info.replace("#EXTINF:-1", f'#EXTINF:-1 group-title="{cat}"')
                                f.write(f"{info}\n{lines[i+1]}\n")
                                total += 1
                except: continue
    print(f"[📡] Radar Latam: {total} canales rescatados para clasificación.")

if __name__ == "__main__":
    rastrear()
