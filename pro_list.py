import requests
import time

BASE_URL = "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/"
EPG_URL = "https://iptv-org.github.io/epg/guides/world.xml.gz"

# Configuración de categorías
categorias = {
    "co": "🇨🇴 COLOMBIA",
    "mx": "🇲🇽 MEXICO",
    "ar": "🇦🇷 ARGENTINA",
    "es": "🇪🇸 ESPAÑA",
    "uk": "🇬🇧 REINO UNIDO",
    "sports": "⚽ DEPORTES",
    "movies": "🎬 PELICULAS",
    "kids": "👶 NIÑOS"
}

headers = {'User-Agent': 'Mozilla/5.0'}

def generar_lista_categorizada():
    print("🗂️ Organizando canales por categorías para Jeycamontv...")
    canales_contados = 0
    
    with open("global_jeycamon.m3u", "w", encoding="utf-8") as f:
        f.write(f'#EXTM3U x-tvg-url="{EPG_URL}"\n')
        
        for cod, nombre_grupo in categorias.items():
            url = f"{BASE_URL}{cod}.m3u"
            print(f"📦 Agregando {nombre_grupo}...", end=" ", flush=True)
            
            try:
                r = requests.get(url, headers=headers, timeout=15)
                if r.status_code == 200:
                    lineas = r.text.splitlines()
                    for i in range(len(lineas)):
                        if lineas[i].startswith("#EXTINF"):
                            # Insertamos la categoría (group-title)
                            info = lineas[i].replace('#EXTINF:-1', f'#EXTINF:-1 group-title="{nombre_grupo}"')
                            f.write(info + "\n")
                            if i + 1 < len(lineas):
                                f.write(lineas[i+1] + "\n")
                                canales_contados += 1
                    print(f"✅")
            except:
                print(f"❌")
            time.sleep(0.5)

    print(f"\n✨ ¡TERMINADO! {canales_contados} canales categorizados.")

if __name__ == "__main__":
    generar_lista_categorizada()

