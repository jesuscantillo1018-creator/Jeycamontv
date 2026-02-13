import requests

# Configuración básica
BASE_STREAMS = "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/"
BASE_CATS = "https://raw.githubusercontent.com/iptv-org/iptv/master/categories/"
EPG_URL = "https://iptv-org.github.io/epg/guides/world.xml.gz"

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

def probar_canal(url):
    """ Intenta conectar con el streaming de video por 3 segundos """
    try:
        # Hacemos una petición 'head' para no descargar el video, solo ver si existe
        response = requests.head(url, headers=headers, timeout=3, allow_redirects=True)
        return response.status_code == 200
    except:
        try:
            # Algunos servidores bloquean 'head', intentamos 'get' limitado
            response = requests.get(url, headers=headers, timeout=3, stream=True)
            return response.status_code == 200
        except:
            return False

def procesar_url(url, nombre_grupo, f, modo_test=False):
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            count = 0
            lineas = r.text.splitlines()
            for i in range(len(lineas)):
                if lineas[i].startswith("#EXTINF"):
                    video_url = lineas[i+1] if i+1 < len(lineas) else ""
                    
                    # Si el modo_test está activo, verificamos canal por canal
                    if modo_test:
                        print(f"🔍 Testeando: {lineas[i].split(',')[-1][:20]}...", end=" ", flush=True)
                        if probar_canal(video_url):
                            print("✅ OK")
                        else:
                            print("❌ CAÍDO")
                            continue # Salta este canal y no lo agrega

                    f.write(lineas[i].replace('#EXTINF:-1', f'#EXTINF:-1 group-title="{nombre_grupo}"') + "\n")
                    f.write(video_url + "\n")
                    count += 1
            print(f"📊 Total funcionales: ({count})")
            return count
        return 0
    except:
        return 0

def generar_lista():
    print("🚀 Iniciando Prototipo Jeycamon con Auto-Test...")
    paises = {"co": "🇨🇴 COLOMBIA", "mx": "🇲🇽 MEXICO", "es": "🇪🇸 ESPAÑA", "us": "🇺🇸 USA"}
    
    with open("global_jeycamon.m3u", "w", encoding="utf-8") as f:
        f.write(f'#EXTM3U x-tvg-url="{EPG_URL}"\n')
        # Los países se cargan rápido (sin test individual para no tardar horas)
        for cod, nombre in paises.items():
            print(f"📡 Cargando {nombre}...", end=" ", flush=True)
            procesar_url(f"{BASE_STREAMS}{cod}.m3u", nombre, f)

if __name__ == "__main__":
    generar_lista()
    print("\n--- 🧐 MODO INVESTIGACIÓN (CON TESTING) ---")
    while True:
        res = input("¿Deseas agregar y testear un link nuevo? (s/n): ").lower()
        if res == 's':
            u = input("🔗 Pega el link RAW: ").strip()
            n = input("🏷️ Nombre de la categoría: ").strip()
            with open("global_jeycamon.m3u", "a", encoding="utf-8") as f:
                # AQUÍ ACTIVAMOS EL TEST (modo_test=True)
                procesar_url(u, f"🔥 {n.upper()}", f, modo_test=True)
        else:
            break
