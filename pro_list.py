import requests

BASE_STREAMS = "https://raw.githubusercontent.com/iptv-org/iptv/master/streams/"
EPG_URL = "https://iptv-org.github.io/epg/guides/world.xml.gz"

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

def validar_canal(url):
    """Prueba si el link de video realmente responde"""
    try:
        # Hacemos una petición rápida (stream) de solo 3 segundos
        r = requests.get(url, headers=headers, timeout=3, stream=True)
        return r.status_code == 200
    except:
        return False

def procesar_url(url, nombre_grupo, f, validar=False):
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            count = 0
            lines = r.text.splitlines()
            for i in range(len(lines)):
                if lines[i].startswith("#EXTINF"):
                    canal_url = lines[i+1] if i+1 < len(lines) else ""
                    
                    # Si activamos validar, probamos el primer canal de la lista
                    if validar and count == 0:
                        print(f"📡 Verificando señal de video...", end=" ", flush=True)
                        if not validar_canal(canal_url):
                            print("⚠️ LISTA POSIBLEMENTE CAÍDA")
                            return 0
                        print("✅ SEÑAL OK")

                    f.write(lines[i].replace('#EXTINF:-1', f'#EXTINF:-1 group-title="{nombre_grupo}"') + "\n")
                    f.write(canal_url + "\n")
                    count += 1
            return count
        return 0
    except:
        return 0

# ... (resto de la lógica de generar_lista igual que antes)
