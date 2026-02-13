import requests
import time

# URLs oficiales verificadas
BASE_STREAMS = "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/"
EPG_URL = "https://iptv-org.github.io/epg/guides/world.xml.gz"

# Mapeo de archivos exactos
paises = {
    "co": "🇨🇴 COLOMBIA", "mx": "🇲🇽 MEXICO", "ar": "🇦🇷 ARGENTINA",
    "es": "🇪🇸 ESPAÑA", "cl": "🇨🇱 CHILE", "pe": "🇵🇪 PERU",
    "ve": "🇻🇪 VENEZUELA", "ec": "🇪🇨 ECUADOR", "uy": "🇺🇾 URUGUAY",
    "do": "🇩🇴 REP. DOMINICANA", "us": "🇺🇸 USA"
}

tematicos = {
    "movies": "🎬 CINE & PELICULAS",
    "animation": "🎎 ANIME & DIBUJOS",
    "kids": "👶 INFANTIL",
    "sports": "⚽ DEPORTES",
    "documentary": "📚 DOCUMENTALES",
    "comedy": "😂 COMEDIA",
    "music": "🎵 MUSICA",
    "news": "📰 NOTICIAS"
}

headers = {'User-Agent': 'Mozilla/5.0'}

def procesar_url(url, nombre_grupo, f):
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            count = 0
            lineas = r.text.splitlines()
            for i in range(len(lineas)):
                if lineas[i].startswith("#EXTINF"):
                    info = lineas[i].replace('#EXTINF:-1', f'#EXTINF:-1 group-title="{nombre_grupo}"')
                    f.write(info + "\n")
                    if i + 1 < len(lineas):
                        f.write(lineas[i+1] + "\n")
                        count += 1
            print(f"✅ ({count} canales)")
            return count
        else:
            print("❌ Error de conexión")
            return 0
    except:
        print("💥 Error crítico")
        return 0

def generar_lista():
    print("🚀 Iniciando Prototipo Jeycamon...")
    canales_totales = 0
    
    with open("global_jeycamon.m3u", "w", encoding="utf-8") as f:
        f.write(f'#EXTM3U x-tvg-url="{EPG_URL}"\n')

        # 1. Países
        for cod, nombre in paises.items():
            url = f"{BASE_STREAMS}{cod}.m3u"
            print(f"📡 {nombre}...", end=" ", flush=True)
            canales_totales += procesar_url(url, nombre, f)

        # 2. Categorías
        for cod, nombre in tematicos.items():
            url = f"https://raw.githubusercontent.com/iptv-org/iptv/master/categories/{cod}.m3u"
            print(f"🌈 {nombre}...", end=" ", flush=True)
            canales_totales += procesar_url(url, nombre, f)
            
    return canales_totales

if __name__ == "__main__":
    total = generar_lista()
    
    # 3. MODO INTERACTIVO
    print("\n--- 🧐 MODO INVESTIGACIÓN ---")
    while True:
        respuesta = input("¿Deseas agregar un link externo nuevo ahora? (s/n): ").lower()
        if respuesta == 's':
            url_ext = input("🔗 Pega el enlace RAW de la lista: ").strip()
            nombre_ext = input("🏷️ Nombre de la categoría (ej. EXTRA): ").strip()
            
            with open("global_jeycamon.m3u", "a", encoding="utf-8") as f:
                print(f"⏳ Verificando {nombre_ext}...", end=" ", flush=True)
                extra = procesar_url(url_ext, f"🔥 {nombre_ext.upper()}", f)
                total += extra
        else:
            break
            
    print(f"\n✅ PROCESO FINALIZADO. Total en lista: {total} canales.")
    print("📂 Archivo generado: global_jeycamon.m3u")

