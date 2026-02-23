import requests

IP = "45.226.168.29"
RUTA = "/movies/"
HEADERS = {'User-Agent': 'Mozilla/5.0'}

# Diccionario de palabras clave (Dorks) para encontrar categorías ocultas
DORKS = {
    "ANIME": ["Anime", "Animes", "Crunchyroll", "DBZ", "Naruto", "Doblado", "Latino"],
    "NOVELAS": ["Novelas", "Telemundo", "Caracol", "RCN", "Televisa", "Series_Latino"],
    "ADULTOS": ["Adultos", "XXX", "Hentai", "Adult", "18+", "Privado", "Premium"],
    "CALIDAD": ["4K", "UltraHD", "Bluray", "Remux"]
}

def escanear():
    print(f"📡 Iniciando escaneo de directorios ocultos en {IP}...\n")
    encontrados = []

    for categoria, palabras in DORKS.items():
        print(f"🕵️ Verificando sección {categoria}...")
        for palabra in palabras:
            # Probamos la palabra como carpeta y como prefijo
            url = f"http://{IP}{RUTA}{palabra}/"
            try:
                r = requests.head(url, headers=HEADERS, timeout=1)
                # 200 (Abierto), 403 (Existe pero prohibido el índice), 301 (Redirige)
                if r.status_code in [200, 403, 301]:
                    print(f"  🔥 ¡POSIBLE CATEGORÍA HALLADA!: {palabra} (Status: {r.status_code})")
                    encontrados.append(palabra)
            except:
                continue
    
    if encontrados:
        print(f"\n✅ Escaneo finalizado. Sugerencia: Usa estos nombres en 'catalogar_todo.py'")
    else:
        print("\n❌ No se hallaron carpetas obvias. El administrador usa nombres personalizados.")

if __name__ == "__main__":
    escanear()
