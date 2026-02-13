import requests
import os
import re

BASE_STREAMS = "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/"
headers = {'User-Agent': 'Mozilla/5.0'}

# Diccionario ampliado con Brasil y otros más
paises = {
    "co": "🇨🇴 COLOMBIA", "mx": "🇲🇽 MEXICO", "ar": "🇦🇷 ARGENTINA", 
    "br": "🇧🇷 BRASIL", "es": "🇪🇸 ESPAÑA", "cl": "🇨🇱 CHILE", 
    "pe": "🇵🇪 PERU", "ve": "🇻🇪 VENEZUELA", "ec": "🇪🇨 ECUADOR",
    "pr": "🇵🇷 PUERTO RICO", "uy": "🇺🇾 URUGUAY", "pa": "🇵🇦 PANAMA",
    "us": "🇺🇸 USA"
}

def procesar_url(url, nombre_grupo_manual, f):
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            count = 0
            lines = r.text.splitlines()
            for i in range(len(lines)):
                if lines[i].startswith("#EXTINF"):
                    linea = lines[i]
                    v_url = lines[i+1].strip() if i+1 < len(lines) else ""
                    if nombre_grupo_manual:
                        linea = re.sub(r'group-title="[^"]*"', '', linea)
                        linea = linea.replace('#EXTINF:-1', f'#EXTINF:-1 group-title="{nombre_grupo_manual}"')
                    f.write(linea + "\n" + v_url + "\n")
                    count += 1
            return count
    except: return 0

def generar_lista():
    print("💎 Construyendo Jeycamon TV PRO con Brasil...")
    with open("global_jeycamon.m3u", "w", encoding="utf-8") as f:
        f.write('#EXTM3U\n')
        if os.path.exists("manuales.m3u"):
            with open("manuales.m3u", "r", encoding="utf-8") as m:
                f.write(m.read())
        for cod, nombre in paises.items():
            print(f"📡 Obteniendo: {nombre}")
            try:
                r = requests.get(f"{BASE_STREAMS}{cod}.m3u", headers=headers, timeout=10)
                if r.status_code == 200:
                    lines = r.text.splitlines()
                    for i in range(len(lines)):
                        if lines[i].startswith("#EXTINF"):
                            f.write(lines[i].replace('#EXTINF:-1', f'#EXTINF:-1 group-title="{nombre}"') + "\n")
                            f.write(lines[i+1] + "\n")
            except: continue

if __name__ == "__main__":
    while True:
        res = input("¿Deseas añadir un link nuevo (Premium/24-7)? (s/n): ").lower()
        if res == 's':
            u = input("🔗 Link RAW: ").strip()
            print("💡 Deja vacío para categorías originales o escribe una (ej: 01-PREMIUM)")
            n = input("🏷️ Categoría: ").strip()
            with open("manuales.m3u", "a", encoding="utf-8") as m:
                cant = procesar_url(u, n.upper() if n else None, m)
                print(f"✅ Se añadieron {cant} canales.")
        else: break
    generar_lista()
    print("🚀 ¡Lista completa con nuevos países generada!")
