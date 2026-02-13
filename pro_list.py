import requests

# URLs base
BASE_STREAMS = "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/"
BASE_CATS = "https://raw.githubusercontent.com/iptv-org/iptv/master/categories/"
EPG_URL = "https://iptv-org.github.io/epg/guides/world.xml.gz"

paises = {
    "co": "🇨🇴 COLOMBIA", "mx": "🇲🇽 MEXICO", "ar": "🇦🇷 ARGENTINA",
    "es": "🇪🇸 ESPAÑA", "cl": "🇨🇱 CHILE", "pe": "🇵🇪 PERU",
    "ve": "🇻🇪 VENEZUELA", "us": "🇺🇸 USA"
}

# Corregidas las rutas para que carguen (ahora usan .m3u directo)
tematicos = {
    "movies": "🎬 CINE", "animation": "🎎 ANIME", "kids": "👶 INFANTIL",
    "sports": "⚽ DEPORTES", "documentary": "📚 DOCS", "news": "📰 NOTICIAS"
}

headers = {'User-Agent': 'Mozilla/5.0'}

def procesar_url(url, nombre_grupo, f):
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            count = 0
            for line in r.text.splitlines():
                if line.startswith("#EXTINF"):
                    f.write(line.replace('#EXTINF:-1', f'#EXTINF:-1 group-title="{nombre_grupo}"') + "\n")
                elif line.startswith("http"):
                    f.write(line + "\n")
                    count += 1
            print(f"✅ ({count})")
            return count
        print("❌")
        return 0
    except:
        print("💥")
        return 0

def generar_lista():
    print("🚀 Iniciando Prototipo Jeycamon...")
    with open("global_jeycamon.m3u", "w", encoding="utf-8") as f:
        f.write(f'#EXTM3U x-tvg-url="{EPG_URL}"\n')
        for cod, nombre in paises.items():
            print(f"📡 {nombre}...", end=" ", flush=True)
            procesar_url(f"{BASE_STREAMS}{cod}.m3u", nombre, f)
        for cod, nombre in tematicos.items():
            print(f"🌈 {nombre}...", end=" ", flush=True)
            procesar_url(f"{BASE_CATS}{cod}.m3u", nombre, f)

if __name__ == "__main__":
    generar_lista()
    print("\n--- 🧐 MODO INVESTIGACIÓN ---")
    while True:
        res = input("¿Deseas agregar un link externo nuevo? (s/n): ").lower()
        if res == 's':
            u = input("🔗 Pega el link RAW: ").strip()
            n = input("🏷️ Nombre de la categoría: ").strip()
            with open("global_jeycamon.m3u", "a", encoding="utf-8") as f:
                procesar_url(u, f"🔥 {n.upper()}", f)
        else:
            break
