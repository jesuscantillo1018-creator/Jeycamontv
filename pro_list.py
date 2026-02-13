import requests
import os
import re

BASE_STREAMS = "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/"
headers = {'User-Agent': 'Mozilla/5.0'}

paises = {
    "co": "🇨🇴 COLOMBIA", "mx": "🇲🇽 MEXICO", "ar": "🇦🇷 ARGENTINA", 
    "es": "🇪🇸 ESPAÑA", "cl": "🇨🇱 CHILE", "pe": "🇵🇪 PERU", "ve": "🇻🇪 VENEZUELA"
}

def obtener_urls_existentes():
    urls = set()
    if os.path.exists("manuales.m3u"):
        with open("manuales.m3u", "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("http"): urls.add(line.strip())
    return urls

def procesar_url(url, nombre_grupo_manual, f, urls_conocidas=None):
    if urls_conocidas is None: urls_conocidas = set()
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            count = 0
            lines = r.text.splitlines()
            for i in range(len(lines)):
                if lines[i].startswith("#EXTINF"):
                    v_url = lines[i+1].strip() if i+1 < len(lines) else ""
                    if v_url in urls_conocidas: continue
                    
                    # 🎯 LÓGICA DE CATEGORÍA INTELIGENTE
                    linea_inf = lines[i]
                    if nombre_grupo_manual:
                        # Si tú escribes una, usamos la tuya
                        nueva_linea = re.sub(r'group-title="[^"]*"', '', linea_inf)
                        nueva_linea = nueva_linea.replace('#EXTINF:-1', f'#EXTINF:-1 group-title="{nombre_grupo_manual}"')
                    else:
                        # Si dejas vacío, intentamos rescatar la original del link
                        if 'group-title="' not in linea_inf:
                            nueva_linea = linea_inf.replace('#EXTINF:-1', f'#EXTINF:-1 group-title="VARIADOS"')
                        else:
                            nueva_linea = linea_inf
                    
                    f.write(nueva_linea + "\n" + v_url + "\n")
                    urls_conocidas.add(v_url)
                    count += 1
            return count
    except: return 0

def generar_lista():
    print("💎 Organizando Jeycamon TV por Categorías...")
    with open("global_jeycamon.m3u", "w", encoding="utf-8") as f:
        f.write('#EXTM3U\n')
        if os.path.exists("manuales.m3u"):
            with open("manuales.m3u", "r", encoding="utf-8") as m:
                f.write(m.read())
        for cod, nombre in paises.items():
            r = requests.get(f"{BASE_STREAMS}{cod}.m3u", headers=headers)
            if r.status_code == 200:
                f.write(r.text.replace("#EXTM3U", "").strip() + "\n")

if __name__ == "__main__":
    generar_lista()
    print("\n--- 🛠️ PANEL DE CONTROL JEYCAMON TV ---")
    while True:
        res = input("¿Deseas añadir un link nuevo? (s/n): ").lower()
        if res == 's':
            u = input("🔗 Link RAW: ").strip()
            print("💡 Si dejas la categoría VACÍA, se respetarán las categorías originales del link.")
            n = input("🏷️ Categoría (o deja vacío): ").strip()
            existentes = obtener_urls_existentes()
            with open("manuales.m3u", "a", encoding="utf-8") as m:
                cant = procesar_url(u, n.upper() if n else None, m, urls_conocidas=existentes)
                print(f"✅ Se procesaron {cant} canales con sus categorías.")
            generar_lista()
        else: break
