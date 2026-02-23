import requests
import os

fuentes_vod = [
    ("https://raw.githubusercontent.com/LaneSh497/Spanish-IPTV-Lists/main/Peliculas.m3u", "ESTRENOS_VOD"),
    ("https://raw.githubusercontent.com/IPTV-Org-Spanish/Latino/main/Animacion.m3u", "ANIMACION"),
    ("http://162.144.133.67/playlist.m3u", "SHODAN_RECAP_USA")
]

def inyectar_vod():
    output_vod = os.path.expanduser("~/iptv/listas_raw/estrenos_vod.m3u")
    total = 0
    print("[🎬] Actualizando fuentes VOD...")
    
    with open(output_vod, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for url, tag in fuentes_vod:
            try:
                r = requests.get(url, timeout=10)
                if r.status_code == 200:
                    lines = r.text.splitlines()
                    for i in range(len(lines)):
                        if lines[i].upper().startswith("#EXTINF"):
                            nombre = lines[i].split(",")[-1]
                            link = lines[i+1] if (i+1 < len(lines)) else ""
                            if link.startswith("http"):
                                f.write(f'#EXTINF:-1 group-title="{tag}",{nombre}\n{link}\n')
                                total += 1
                print(f"[✔] {tag} procesada.")
            except:
                print(f"[!] Error en fuente: {tag}")
    print(f"[⭐] Inyección terminada: {total} posibles candidatos.")

if __name__ == "__main__":
    inyectar_vod()
