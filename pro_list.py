import requests
import time

BASE_STREAMS = "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/"
BASE_CATEGORIES = "https://raw.githubusercontent.com/iptv-org/iptv/master/categories/"
EPG_URL = "https://iptv-org.github.io/epg/guides/world.xml.gz"

# Separamos fuentes por tipo
paises = {
    "co": "🇨🇴 COLOMBIA", "mx": "🇲🇽 MEXICO", "ar": "🇦🇷 ARGENTINA", 
    "es": "🇪🇸 ESPAÑA", "cl": "🇨🇱 CHILE", "pe": "🇵🇪 PERU", 
    "ve": "🇻🇪 VENEZUELA", "ec": "🇪🇨 ECUADOR", "uy": "🇺🇾 URUGUAY", 
    "do": "🇩🇴 REP. DOMINICANA", "us": "🇺🇸 USA"
}

tematicos = {
    "movies": "🎬 CINE & PELICULAS", "series": "📺 SERIES TV", 
    "animation": "🎎 ANIME & DIBUJOS", "kids": "👶 INFANTIL", 
    "sports": "⚽ DEPORTES", "documentary": "📚 DOCUMENTALES", 
    "comedy": "😂 COMEDIA", "music": "🎵 MUSICA", "news": "📰 NOTICIAS"
}

headers = {'User-Agent': 'Mozilla/5.0'}

def generar_lista():
    print("🚀 Buscando canales en Países y Categorías...")
    canales_contados = 0
    
    with open("global_jeycamon.m3u", "w", encoding="utf-8") as f:
        f.write(f'#EXTM3U x-tvg-url="{EPG_URL}"\n')
        
        # 1. Buscar Países
        for cod, nombre in paises.items():
            url = f"{BASE_STREAMS}{cod}.m3u"
            print(f"📡 {nombre}...", end=" ", flush=True)
            canales_contados += procesar_url(url, nombre, f)

        # 2. Buscar Categorías
        for cod, nombre in tematicos.items():
            url = f"{BASE_CATEGORIES}{cod}.m3u"
            print(f"🌈 {nombre}...", end=" ", flush=True)
            canales_contados += procesar_url(url, nombre, f)

    print(f"\n✅ ¡SÚPER LISTA TERMINADA! Total: {canales_contados} canales.")

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
            print("✅")
            return count
        else:
            print("❌")
            return 0
    except:
        print("💥")
        return 0

if __name__ == "__main__":
    generar_lista()
