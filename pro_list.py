import requests
import time

# Usamos la API de categorías y países de iptv-org
BASE_URL = "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/"
EPG_URL = "https://iptv-org.github.io/epg/guides/world.xml.gz"

# CORRECCIÓN DE ETIQUETAS: Nombres exactos de los archivos en GitHub
categorias = {
    "co": "🇨🇴 COLOMBIA",
    "mx": "🇲🇽 MEXICO",
    "ar": "🇦🇷 ARGENTINA",
    "es": "🇪🇸 ESPAÑA",
    "cl": "🇨🇱 CHILE",
    "pe": "🇵🇪 PERU",
    "ve": "🇻🇪 VENEZUELA",
    "ec": "🇪🇨 ECUADOR",
    "uy": "🇺🇾 URUGUAY",
    "do": "🇩🇴 REP. DOMINICANA",
    "us": "🇺🇸 USA (General)",
    "movie": "🎬 CINE & PELICULAS",
    "series": "📺 SERIES TV",
    "animation": "🎎 ANIME & DIBUJOS",
    "kids": "👶 INFANTIL",
    "sports": "⚽ DEPORTES",
    "documentary": "📚 DOCUMENTALES",
    "comedy": "😂 COMEDIA",
    "music": "🎵 MUSICA",
    "news": "📰 NOTICIAS"
}

headers = {'User-Agent': 'Mozilla/5.0'}

def generar_lista():
    print("🔥 Reparando categorías y buscando canales nuevos...")
    canales_contados = 0
    
    with open("global_jeycamon.m3u", "w", encoding="utf-8") as f:
        f.write(f'#EXTM3U x-tvg-url="{EPG_URL}"\n')
        
        for cod, nombre_grupo in categorias.items():
            url = f"{BASE_URL}{cod}.m3u"
            print(f"📡 Buscando {nombre_grupo}...", end=" ", flush=True)
            
            try:
                r = requests.get(url, headers=headers, timeout=15)
                if r.status_code == 200:
                    lineas = r.text.splitlines()
                    for i in range(len(lineas)):
                        if lineas[i].startswith("#EXTINF"):
                            # Limpieza de etiquetas para IPTV Smarters
                            info = lineas[i].replace('#EXTINF:-1', f'#EXTINF:-1 group-title="{nombre_grupo}"')
                            f.write(info + "\n")
                            if i + 1 < len(lineas):
                                f.write(lineas[i+1] + "\n")
                                canales_contados += 1
                    print(f"✅")
                else:
                    # Intento alternativo para categorías que terminan en 's' o no
                    print(f"⚠️ Reintentando...")
                    alt_url = url.replace(".m3u", "s.m3u") if not url.endswith("s.m3u") else url.replace("s.m3u", ".m3u")
                    r_alt = requests.get(alt_url, headers=headers, timeout=10)
                    if r_alt.status_code == 200:
                        # (Mismo proceso de guardado)
                        lineas = r_alt.text.splitlines()
                        for i in range(len(lineas)):
                            if lineas[i].startswith("#EXTINF"):
                                info = lineas[i].replace('#EXTINF:-1', f'#EXTINF:-1 group-title="{nombre_grupo}"')
                                f.write(info + "\n")
                                if i + 1 < len(lineas):
                                    f.write(lineas[i+1] + "\n")
                                    canales_contados += 1
                        print(f"  └─ ✅ Encontrado!")
                    else:
                        print(f"  └─ ❌ No disponible")
            except:
                print(f"💥 Error")
            time.sleep(0.2)

    print(f"\n🚀 ¡SÚPER LISTA LISTA! Total: {canales_contados} canales.")

if __name__ == "__main__":
    generar_lista()
