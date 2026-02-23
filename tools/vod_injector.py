import requests
import os

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

fuentes = {
    "DEPORTES_WIN": ["https://raw.githubusercontent.com/LaneSh497/Spanish-IPTV-Lists/main/Deportes.m3u"],
    "CINE_HBO_NETFLIX": ["https://raw.githubusercontent.com/Iptv-org-spanish/Peliculas/main/Peliculas.m3u"],
    "COLOMBIA_NOVELAS": ["https://raw.githubusercontent.com/iptv-org/iptv/master/streams/co.m3u"],
    "XXX_ADULTOS": ["https://raw.githubusercontent.com/Iptv-org-spanish/Adultos/main/Adultos.m3u"],
    "CANALES_24_7": ["https://raw.githubusercontent.com/Iptv-org-spanish/24-7/main/24-7.m3u"],
    "ANIME_SERIES": ["https://raw.githubusercontent.com/Jesustv/Programas/master/Anime.m3u"]
}

def inyectar():
    output = os.path.expanduser("~/iptv/listas_raw/estrenos_vod.m3u")
    win_local = os.path.expanduser("~/iptv/listas_raw/winplaycol.m3u")
    total = 0
    
    with open(output, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        
        # Win Local
        if os.path.exists(win_local):
            with open(win_local, "r") as wl:
                f.write(wl.read().replace("#EXTM3U\n", ""))
                total += 10
        
        # Externos
        for cat, urls in fuentes.items():
            for url in urls:
                try:
                    r = requests.get(url, headers=headers, timeout=15)
                    if r.status_code == 200:
                        lines = r.text.splitlines()
                        for i in range(len(lines)):
                            if lines[i].upper().startswith("#EXTINF"):
                                info = lines[i]
                                if 'group-title' not in info:
                                    info = info.replace("#EXTINF:-1", f'#EXTINF:-1 group-title="{cat}"')
                                f.write(f"{info}\n{lines[i+1]}\n")
                                total += 1
                except: continue
    print(f"[⭐] Radar finalizado. Candidatos: {total}")

if __name__ == "__main__":
    inyectar()
