import requests
import os

fuentes = [
    ("https://iptv-org.github.io/iptv/countries/mx.m3u", "MEXICO_ORG"),
    ("https://iptv-org.github.io/iptv/countries/es.m3u", "ESPAÑA_ORG"),
    ("https://raw.githubusercontent.com/fomny/fomny-iptv/main/main.m3u", "INTERNACIONAL_VOD"),
    ("https://raw.githubusercontent.com/TukAn0/IPTV/master/IPTV_M3U", "LATAM_MIX")
]

def descargar_y_unir():
    output_raw = os.path.expanduser("~/iptv/listas_raw/mega_import.m3u")
    total = 0
    print("[🚀] Iniciando importación masiva...")
    
    with open(output_raw, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for url, tag in fuentes:
            try:
                r = requests.get(url, timeout=10)
                if r.status_code == 200:
                    lines = r.text.splitlines()
                    for i in range(len(lines)):
                        if lines[i].startswith("#EXTINF"):
                            # Inyectamos el tag para que aparezca en tu JSON
                            f.write(lines[i].replace("#EXTINF:-1", f'#EXTINF:-1 group-title="{tag}"') + "\n")
                            if i+1 < len(lines):
                                f.write(lines[i+1] + "\n")
                                total += 1
                print(f"[+] {tag}: {total} canales importados.")
            except:
                print(f"[!] Error en fuente: {tag}")

    print(f"\n[✔] ¡Mega Importación lista! Total: {total} canales nuevos.")

if __name__ == "__main__":
    descargar_y_unir()
