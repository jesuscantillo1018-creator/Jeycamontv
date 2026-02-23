import re
import os

def asignar_categoria(nombre_canal):
    n = nombre_canal.upper()
    
    # Categorías Especiales
    if any(k in n for k in ["WIN", "ESPN", "FOX SPORT", "DIRECTV", "GOL", "FUTBOL", "NBA", "F1", "WIN+"]):
        return "DEPORTES 🏆"
    if any(k in n for k in ["HBO", "CINEMA", "MOVIES", "STAR+", "CINE", "WARNER", "TNT", "PARAMOUNT", "FILM"]):
        return "PELICULAS 🎬"
    if any(k in n for k in ["NETFLIX", "APPLE TV", "AMAZON", "AMC", "SERIE"]):
        return "SERIES 📺"
    if any(k in n for k in ["PLAYBOY", "VENUS", "ADULT", "BRAZZERS", "HUSTLER", "PENTHOUSE", "XXX", "X-TIME"]):
        return "CONTENIDO ADULTO (18+) 🔞"
    if any(k in n for k in ["DISNEY", "NICKELODEON", "CARTOON", "KIDS", "DISCOVERY KIDS", "BOOMERANG"]):
        return "INFANTIL 🧸"
    if any(k in n for k in ["ANIME", "TOONCAST", "CRUNCHYROLL"]):
        return "ANIME ⛩️"
    if any(k in n for k in ["CARACOL", "RCN", "NOVELA", "PASIONES", "TELEMUNDO", "TLNOVELAS"]):
        return "NOVELAS 🎭"
    
    # Categorías por País
    if "(CO)" in n or "COLOMBIA" in n: return "COLOMBIA 🇨🇴"
    if "(MX)" in n or "MEXICO" in n: return "MEXICO 🇲🇽"
    if "(AR)" in n or "ARGENTINA" in n: return "ARGENTINA 🇦🇷"
    if "(ES)" in n or "ESPANA" in n or "ESPAÑA" in n: return "ESPAÑA 🇪🇸"
    if "(US)" in n or "USA" in n or "UNITED STATES" in n: return "USA 🇺🇸"
    if "(CL)" in n or "CHILE" in n: return "CHILE 🇨🇱"
    
    return "VARIADOS 🌐"

def procesar_lista():
    input_file = "global_jeycamon.m3u"
    output_file = "global_jeycamon.m3u"
    
    if not os.path.exists(input_file):
        print(f"Error: No se encontró {input_file}")
        return

    with open(input_file, 'r', encoding='utf-8') as f:
        lineas = f.readlines()

    canales_limpios = []
    header = "#EXTM3U\n"
    
    current_info = ""
    for linea in lineas:
        linea = linea.strip()
        if linea.startswith("#EXTINF"):
            # Extraer el nombre del canal
            nombre = linea.split(",")[-1]
            categoria = asignar_categoria(nombre)
            
            # Limpiar etiquetas viejas de group-title si existen y poner la nueva
            linea_limpia = re.sub(r'group-title=".*?"', '', linea)
            linea_limpia = linea_limpia.replace("#EXTINF:-1", f'#EXTINF:-1 group-title="{categoria}"')
            current_info = linea_limpia
        elif linea.startswith("http"):
            if current_info:
                canales_limpios.append(f"{current_info}\n{linea}\n")
                current_info = ""

    # Eliminar duplicados manteniendo el orden
    canales_unicos = list(dict.fromkeys(canales_limpios))

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(header)
        for canal in canales_unicos:
            f.write(canal)
    
    print(f"✅ Lista organizada: {len(canales_unicos)} canales categorizados.")

if __name__ == "__main__":
    procesar_lista()
