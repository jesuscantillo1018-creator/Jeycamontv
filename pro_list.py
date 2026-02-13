import requests
import os

BASE_STREAMS = "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/"
EPG_URL = "https://iptv-org.github.io/epg/guides/world.xml.gz"
headers = {'User-Agent': 'Mozilla/5.0'}

paises = {
    "co": "🇨🇴 COLOMBIA", "mx": "🇲🇽 MEXICO", "ar": "🇦🇷 ARGENTINA", 
    "es": "🇪🇸 ESPAÑA", "cl": "🇨🇱 CHILE", "pe": "🇵🇪 PERU", 
    "ve": "🇻🇪 VENEZUELA", "ec": "🇪🇨 ECUADOR", "uy": "🇺🇾 URUGUAY", 
    "do": "🇩🇴 REP. DOMINICANA", "us": "🇺🇸 USA", "br": "🇧🇷 BRASIL",
    "pa": "🇵🇦 PANAMA", "cr": "🇨🇷 COSTA RICA", "py": "🇵🇾 PARAGUAY"
}

def probar_canal(url):
    try:
        r = requests.get(url, headers=headers, timeout=5, stream=True)
        return r.status_code == 200
    except:
        return False

def obtener_urls_existentes():
    urls = set()
    if os.path.exists("manuales.m3u"):
        with open("manuales.m3u", "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("http"):
                    urls.add(line.strip())
    return urls

def procesar_url(url, nombre_grupo, f, modo_test=False, urls_conocidas=None):
    if urls_conocidas is None: urls_conocidas = set()
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            count = 0
            lines = r.text.splitlines()
            saltar_test = "XXX" in nombre_grupo.upper()
            
            for i in range(len(lines)):
                if lines[i].startswith("#EXTINF"):
                    v_url = lines[i+1].strip() if i+1 < len(lines) else ""
                    
                    # 🛡️ FILTRO DE DUPLICADOS
                    if v_url in urls_conocidas:
                        continue
                    
                    if modo_test and not saltar_test:
                        print(f"🔍 Test: {lines[i].split(',')[-1][:15]}...", end=" ", flush=True)
                        if not probar_canal(v_url):
                            print("❌")
                            continue
                        print("✅ OK")
                    elif saltar_test:
                        print(f"📥 Agregando: {lines[i].split(',')[-1][:15]}...")
                    
                    f.write(lines[i].replace('#EXTINF:-1', f'#EXTINF:-1 group-title="{nombre_grupo}"') + "\n")
                    f.write(v_url + "\n")
                    urls_conocidas.add(v_url)
                    count += 1
            return count
        return 0
    except:
        return 0

def generar_lista():
    print("🚀 Cargando canales de Países...")
    with open("global_jeycamon.m3u", "w", encoding="utf-8") as f:
        f.write(f'#EXTM3U x-tvg-url="{EPG_URL}"\n')
        for cod, nombre in paises.items():
            procesar_url(f"{BASE_STREAMS}{cod}.m3u", nombre, f)
        if os.path.exists("manuales.m3u"):
            with open("manuales.m3u", "r", encoding="utf-8") as m:
                f.write(m.read())

if __name__ == "__main__":
    generar_lista()
    print("\n--- 🧐 MODO INVESTIGACIÓN ---")
    while True:
        res = input("¿Deseas agregar algo NUEVO? (s/n): ").lower()
        if res == 's':
            u = input("🔗 Link RAW: ").strip()
            n = input("🏷️ Categoría: ").strip()
            existentes = obtener_urls_existentes()
            with open("manuales.m3u", "a", encoding="utf-8") as m:
                cant = procesar_url(u, f"🔥 {n.upper()}", m, modo_test=True, urls_conocidas=existentes)
                print(f"✨ Se agregaron {cant} canales nuevos (sin repetir).")
            generar_lista()
        else:
            break
