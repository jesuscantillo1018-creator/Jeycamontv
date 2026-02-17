import requests
import re

# Configuración
IP = "45.226.168.29"
RUTA = "/movies/"
NOMBRE_ARCHIVO = "series_premium.m3u"
HEADERS = {'User-Agent': 'Mozilla/5.0'}

# Lista base de series (puedes dejar algunas fijas)
SERIES_FIJAS = ["TheLastOfUs", "Fallout", "Halo", "Yellowstone"]

def limpiar_nombre_serie(texto, s, e):
    base = re.sub(r'([a-z])([A-Z0-8])', r'\1 \2', texto).title()
    return f"{base} - S{s:02d}E{e:02d}"

def buscar_serie(serie_nombre, archivo_f):
    print(f"\n🔍 Buscando capítulos de: {serie_nombre}...")
    encontrados_serie = 0
    # Probamos 3 temporadas y 15 episodios por temporada
    for s in range(1, 4):
        caps_en_temporada = 0
        for e in range(1, 16):
            formatos = [
                f"{serie_nombre}_S{s:02d}E{e:02d}.mp4",
                f"{serie_nombre}S{s:02d}E{e:02d}.mp4"
            ]
            hallado = False
            for intento in formatos:
                url = f"http://{IP}{RUTA}{intento}"
                try:
                    r = requests.head(url, headers=HEADERS, timeout=0.8)
                    if r.status_code == 200:
                        nombre_bonito = limpiar_nombre_serie(serie_nombre, s, e)
                        archivo_f.write(f'#EXTINF:-1 tvg-name="{nombre_bonito}" group-title="📺 JEYCAMON SERIES",{nombre_bonito}\n')
                        archivo_f.write(f'{url}\n')
                        print(f"  ✅ {nombre_bonito}")
                        encontrados_serie += 1
                        caps_en_temporada += 1
                        hallado = True
                        break
                except: continue
            
            # Si no halla el episodio 1 y 2, saltar temporada para ahorrar tiempo
            if not hallado and e > 2 and caps_en_temporada == 0:
                break
    return encontrados_serie

def main():
    print("📺 --- BIENVENIDO AL BUSCADOR INTERACTIVO JEYCAMON --- 📺")
    
    # Preguntar por series nuevas
    nuevas = []
    while True:
        opcion = input("\n¿Quieres agregar una serie nueva para buscar? (s/n): ").lower()
        if opcion == 's':
            nombre = input("Escribe el nombre de la serie (Ej: CobraKai): ").strip()
            if nombre: nuevas.append(nombre)
        else:
            break

    lista_total = SERIES_FIJAS + nuevas
    total_global = 0

    with open(NOMBRE_ARCHIVO, "w") as f:
        f.write("#EXTM3U\n")
        for s in lista_total:
            total_global += buscar_serie(s, f)

    print(f"\n🚀 Magia terminada. Se encontraron {total_global} capítulos en total.")

if __name__ == "__main__":
    main()
