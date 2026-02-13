import requests
import os

BASE_STREAMS = "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/"
EPG_URL = "https://iptv-org.github.io/epg/guides/world.xml.gz"
headers = {'User-Agent': 'Mozilla/5.0'}

def probar_canal(url):
    try:
        r = requests.head(url, headers=headers, timeout=3)
        return r.status_code == 200
    except:
        return False

def procesar_url(url, nombre_grupo, f, modo_test=False):
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            count = 0
            lines = r.text.splitlines()
            for i in range(len(lines)):
                if lines[i].startswith("#EXTINF"):
                    v_url = lines[i+1] if i+1 < len(lines) else ""
                    if modo_test:
                        print(f"🔍 Test: {lines[i].split(',')[-1][:15]}...", end=" ", flush=True)
                        if not probar_canal(v_url):
                            print("❌")
                            continue
                        print("✅")
                    f.write(lines[i].replace('#EXTINF:-1', f'#EXTINF:-1 group-title="{nombre_grupo}"') + "\n")
                    f.write(v_url + "\n")
                    count += 1
            return count
        return 0
    except:
        return 0

def generar_lista():
    print("🚀 Cargando base de países...")
    paises = {"co": "🇨🇴 COLOMBIA", "mx": "🇲🇽 MEXICO", "es": "🇪🇸 ESPAÑA", "us": "🇺🇸 USA"}
    with open("global_jeycamon.m3u", "w", encoding="utf-8") as f:
        f.write(f'#EXTM3U x-tvg-url="{EPG_URL}"\n')
        for cod, nombre in paises.items():
            procesar_url(f"{BASE_STREAMS}{cod}.m3u", nombre, f)
        
        # AQUÍ ESTÁ EL TRUCO: Leer canales guardados anteriormente
        if os.path.exists("manuales.m3u"):
            print("cargando canales guardados previamente... ✅")
            with open("manuales.m3u", "r") as m:
                f.write(m.read())

if __name__ == "__main__":
    generar_lista()
    print("\n--- 🧐 MODO INVESTIGACIÓN ---")
    while True:
        res = input("¿Deseas agregar algo NUEVO? (s/n): ").lower()
        if res == 's':
            u = input("🔗 Link RAW: ").strip()
            n = input("🏷️ Categoría: ").strip()
            # Guardamos en el archivo permanente para que no se borre nunca
            with open("manuales.m3u", "a", encoding="utf-8") as m:
                procesar_url(u, f"🔥 {n.upper()}", m, modo_test=True)
            # Re-generamos la lista principal para incluir lo nuevo
            generar_lista()
        else:
            break
