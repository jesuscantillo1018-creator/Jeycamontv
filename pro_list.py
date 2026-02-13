import requests
import os

BASE_STREAMS = "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/"
headers = {'User-Agent': 'Mozilla/5.0'}

# Definición estricta de países con sus etiquetas
paises = {
    "co": "🇨🇴 COLOMBIA", "mx": "🇲🇽 MEXICO", "ar": "🇦🇷 ARGENTINA", 
    "es": "🇪🇸 ESPAÑA", "cl": "🇨🇱 CHILE", "pe": "🇵🇪 PERU", 
    "ve": "🇻🇪 VENEZUELA", "ec": "🇪🇨 ECUADOR", "us": "🇺🇸 USA"
}

def generar_lista():
    print("💎 Reconstruyendo categorías Jeycamon TV...")
    with open("global_jeycamon.m3u", "w", encoding="utf-8") as f:
        f.write('#EXTM3U\n')
        
        # 1. Cargar manuales si existen
        if os.path.exists("manuales.m3u"):
            with open("manuales.m3u", "r", encoding="utf-8") as m:
                f.write(m.read() + "\n")
        
        # 2. Cargar PAÍSES forzando la categoría
        for cod, nombre_grupo in paises.items():
            print(f"📡 Organizando {nombre_grupo}...")
            try:
                r = requests.get(f"{BASE_STREAMS}{cod}.m3u", headers=headers, timeout=10)
                if r.status_code == 200:
                    lines = r.text.splitlines()
                    for i in range(len(lines)):
                        if lines[i].startswith("#EXTINF"):
                            # Esta línea es la que pone la bandera y el nombre del país
                            info = lines[i].replace('#EXTINF:-1', f'#EXTINF:-1 group-title="{nombre_grupo}"')
                            f.write(info + "\n")
                            if i + 1 < len(lines):
                                f.write(lines[i+1] + "\n")
            except:
                continue

if __name__ == "__main__":
    generar_lista()
    print("\n✅ ¡Categorías restauradas!")
