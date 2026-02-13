import requests
import time

# Lista de países (puedes añadir más como 'it', 'fr', 'br', etc.)
paises = ["co", "ar", "mx", "es", "us", "cl"]
base_url = "https://raw.githubusercontent.com/jesuscantillo1018-creator/Jeycamontv/maestro/streams/"

# Es vital añadir esto para que GitHub no nos bloquee
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def crear_lista_global():
    with open("global_jeycamon.m3u", "w", encoding="utf-8") as f_out:
        f_out.write("#EXTM3U\n")
        
        for p in paises:
            url = f"{base_url}{p}.m3u"
            print(f"Procesando {p}...", end=" ")
            
            try:
                r = requests.get(url, headers=headers, timeout=10)
                if r.status_code == 200:
                    lineas = r.text.split("\n")
                    # Filtramos las líneas vacías y la cabecera repetida
                    enlaces_agregados = 0
                    for linea in lineas:
                        if linea.strip() and not linea.startswith("#EXTM3U"):
                            f_out.write(linea.strip() + "\n")
                            enlaces_agregados += 1
                    print(f"✅ ({enlaces_agregados} links)")
                else:
                    print(f"❌ Error {r.status_code}")
                
                # Pausa de medio segundo para no saturar
                time.sleep(0.5)
                
            except Exception as e:
                print(f"❌ Fallo de conexión: {e}")

if __name__ == "__main__":
    crear_lista_global()
    print("\nArchivo 'global_jeycamon.m3u' generado con éxito.")
