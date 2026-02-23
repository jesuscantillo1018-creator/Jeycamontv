import json
import os
import re
import requests

# --- CONFIGURACIÓN ---
TMDB_API_KEY = "c7e63111007cf1aea6b2323003de6a4a"
BASE_DIR = os.path.expanduser("~/iptv")
GLOBAL_M3U = os.path.join(BASE_DIR, "global_jeycamon.m3u")
OUTPUT_JSON = os.path.join(BASE_DIR, "jeycamon.json")

# Imagen elegante de respaldo si no hay logo
IMG_BACKUP = "https://i.imgur.com/8N3S3X8.png" 

def buscar_en_tmdb(nombre_limpio):
    for tipo in ["movie", "tv"]:
        url = f"https://api.themoviedb.org/3/search/{tipo}?api_key={TMDB_API_KEY}&query={nombre_limpio}&language=es-ES"
        try:
            r = requests.get(url, timeout=5).json()
            if r.get('results'):
                data = r['results'][0]
                poster = f"https://image.tmdb.org/t/p/w500{data['poster_path']}" if data.get('poster_path') else None
                backdrop = f"https://image.tmdb.org/t/p/original{data['backdrop_path']}" if data.get('backdrop_path') else None
                sinopsis = data.get('overview', 'Disfruta de este contenido en Jeycamon TV.')
                rating = data.get('vote_average', 0)
                year = data.get('release_date', '2026')[:4] if tipo == "movie" else data.get('first_air_date', '2026')[:4]
                return poster, backdrop, sinopsis, rating, year
        except:
            continue
    return None, None, None, None, None

def generar_json_pro():
    print("\n[💎] PANEL PROFESIONAL: Optimizando Estética y Metadatos...")
    canales = []
    
    if not os.path.exists(GLOBAL_M3U): return

    with open(GLOBAL_M3U, "r", encoding="utf-8") as f:
        content = f.read()
        bloques = re.split(r'#EXTINF', content)[1:]
        
        for bloque in bloques:
            try:
                lineas = bloque.strip().split('\n')
                info_line = lineas[0]
                url = lineas[1].strip()
                
                # Nombre original y limpieza
                nombre_raw = info_line.split(',')[-1].strip()
                cat_match = re.search(r'group-title="([^"]+)"', info_line)
                categoria = cat_match.group(1) if cat_match else "VARIOS"
                
                # Tags de calidad automáticos para la vista del cliente
                calidad = "HD"
                if "4K" in nombre_raw.upper() or "UHD" in nombre_raw.upper(): calidad = "4K"
                elif "720" in nombre_raw.upper(): calidad = "SD"

                nombre_busqueda = re.sub(r'\[.*?\]|\(.*?\)|\d{3,4}p|HD|FULL|4K|\.mp4|\.mkv', '', nombre_raw).strip()
                
                # Valores por defecto profesionales
                poster_final = IMG_BACKUP
                fondo_pantalla = ""
                descripcion = "Contenido Premium verificado por Jeycamon TV."
                estrellas = 5.0
                año = "2026"

                # Lógica TMDB para VOD
                if any(x in categoria.upper() for x in ["CINE", "NETFLIX", "HBO", "SERIES", "VOD", "MOVIES"]):
                    p, b, d, r, y = buscar_en_tmdb(nombre_busqueda)
                    if p:
                        poster_final, fondo_pantalla, descripcion, estrellas, año = p, b, d, r, y
                        print(f"  [🎬] Match Profesional: {nombre_busqueda} ({año})")
                else:
                    # Para Canales de TV: Intentamos capturar logo del M3U
                    logo_match = re.search(r'tvg-logo="([^"]+)"', info_line)
                    if logo_match: poster_final = logo_match.group(1)

                canales.append({
                    "name": nombre_raw,
                    "clean_name": nombre_busqueda,
                    "url": url,
                    "category": categoria,
                    "logo": poster_final,
                    "backdrop": fondo_pantalla,
                    "description": descripcion,
                    "rating": estrellas,
                    "year": año,
                    "quality": calidad,
                    "provider": "Jeycamon TV"
                })
            except: continue

    with open(OUTPUT_JSON, "w", encoding="utf-8") as jf:
        json.dump({"provider_info": {"name": "Jeycamon TV", "status": "Online"}, "channels": canales}, jf, indent=4, ensure_ascii=False)
    
    print(f"\n[✅] PANEL ACTUALIZADO: {len(canales)} canales con estética Pro.")

if __name__ == "__main__":
    generar_json_pro()
