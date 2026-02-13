import requests
import time

BASE_URL = "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/"
EPG_URL = "https://iptv-org.github.io/epg/guides/world.xml.gz"

# Categorías exhaustivas: Países, USA Latino, Novelas, Cine y Series
categorias = {
    "co": "🇨🇴 COLOMBIA",
    "mx": "🇲🇽 MEXICO",
    "us_itv": "🇺🇸 USA LATINO (Premium)",
    "us_spanish": "🇺🇸 USA ESPAÑOL",
    "ar": "🇦🇷 ARGENTINA",
    "es": "🇪🇸 ESPAÑA",
    "cl": "🇨🇱 CHILE",
    "pe": "🇵🇪 PERU",
    "ve": "🇻🇪 VENEZUELA",
    "ec": "🇪🇨 ECUADOR",
    "uy": "🇺🇾 URUGUAY",
    "do": "🇩🇴 REP. DOMINICANA",
    "movies": "🎬 CINE & PELICULAS",
    "series": "📺 SERIES TV",
    "novelas": "💖 NOVELAS",
    "animation": "🎎 ANIME & DIBUJOS",
    "kids": "👶 INFANTIL (Cartoon)",
    "sports": "⚽ DEPORTES",
    "documentary": "📚 DOCUMENTALES",
    "comedy": "😂 COMEDIA",
    "music": "🎵 MUSICA",
    "news": "📰 NOTICIAS"
}

headers = {'User-Agent': 'Mozilla/5.0'}

def generar_lista_total_espanol():
    print("🔥 Generando la lista definitiva Jeycamontv...")
    print("Buscando Películas, Series, Novelas y canales de USA en Español...")
    canales_contados = 0
    
    with open("global_jeycamon.m3u", "w", encoding="utf-8") as f:
        f.write(f'#EXTM3U x-tvg-url="{EPG_URL}"\n')
        
        for cod, nombre_grupo in categorias.items():
            url = f"{BASE_URL}{cod}.m3u"
            print(f"📡 Importando {nombre_grupo}...", end=" ", flush=True)
            
            try:
                r = requests.get(url, headers=headers, timeout=15)
                if r.status_code == 200:
                    lineas = r.text.splitlines()
                    for i in range(len(lineas)):
                        if lineas[i].startswith("#EXTINF"):
                            # Agregamos la categoría (group-title)
                            info = lineas[i].replace('#EXTINF:-1', f'#EXTINF:-1 group-title="{nombre_grupo}"')
                            f.write(info + "\n")
                            if i + 1 < len(lineas):
                                f.write(lineas[i+1] + "\n")
                                canales_contados += 1
                    print(f"✅")
                else:
                    print(f"⚠️ (No disponible)")
            except:
                print(f"💥 Error de conexión")
            time.sleep(0.3) # Un poco más rápido

    print(f"\n🚀 ¡LISTO! Tu servidor ahora tiene {canales_contados} canales.")
    print("Ejecuta ./actualizar.sh para subir los cambios.")

if __name__ == "__main__":
    generar_lista_total_espanol()
