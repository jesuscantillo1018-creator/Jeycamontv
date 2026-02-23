import requests
import time

# Usamos la base de datos central de iptv-org para asegurar que los archivos existan
BASE_URL = "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/"

# Lista extendida con las rutas REALES del repositorio
categorias = [
    "co", "mx", "ar", "es", "cl", "pe", "br",  # Latino y España
    "us_itv", "uk", "ca",                      # Inglés
    "sports", "movies", "news", "kids"         # Temáticos
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/110.0.0.0 Safari/537.36'
}

def generar_m3u_global():
    print("🚀 Iniciando recolección global para JeycamonTV...")
    canales_totales = 0
    
    with open("global_jeycamon.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        
        for cat in categorias:
            url = f"{BASE_URL}{cat}.m3u"
            print(f"📡 Descargando {cat}...", end=" ", flush=True)
            
            try:
                r = requests.get(url, headers=headers, timeout=15)
                if r.status_code == 200:
                    lineas = r.text.splitlines()
                    agregados = 0
                    for line in lineas:
                        if line.strip() and not line.startswith("#EXTM3U"):
                            f.write(line + "\n")
                            if line.startswith("#EXTINF"): 
                                agregados += 1
                    canales_totales += agregados
                    print(f"✅ +{agregados} canales.")
                else:
                    print(f"❌ Error {r.status_code} (Ruta no válida)")
            except:
                print("💥 Error de conexión.")
            
            time.sleep(0.8) # Para evitar bloqueos de seguridad

    print(f"\n✨ ¡Éxito! Archivo 'global_jeycamon.m3u' creado con {canales_totales} canales.")

if __name__ == "__main__":
    generar_m3u_global()
