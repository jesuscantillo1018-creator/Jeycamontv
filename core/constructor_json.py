import json
import os
import re
import requests

# --- CONFIGURACIÓN ---
TMDB_API_KEY = "c7e63111007cf1aea6b2323003de6a4a"
BASE_DIR = os.path.expanduser("~/iptv")
GLOBAL_M3U_TEMP = os.path.join(BASE_DIR, "global_jeycamon.m3u_temp")
GLOBAL_M3U_FINAL = os.path.join(BASE_DIR, "global_jeycamon.m3u")
OUTPUT_JSON = os.path.join(BASE_DIR, "jeycamon.json")

def buscar_en_tmdb(nombre_limpio):
    for tipo in ["movie", "tv"]:
        url = f"https://api.themoviedb.org/3/search/{tipo}?api_key={TMDB_API_KEY}&query={nombre_limpio}&language=es-ES"
        try:
            r = requests.get(url, timeout=5).json()
            if r.get('results'):
                data = r['results'][0]
                poster = f"https://image.tmdb.org/t/p/w500{data['poster_path']}" if data.get('poster_path') else None
                return poster
        except: continue
    return None

def generar_todo():
    print("\n[🎨] RECONSTRUCCIÓN ESTÉTICA TOTAL...")
    canales_m3u = ["#EXTM3U\n"]
    
    if not os.path.exists(GLOBAL_M3U_TEMP): return

    with open(GLOBAL_M3U_TEMP, "r", encoding="utf-8") as f:
        content = f.read()
        bloques = re.split(r'#EXTINF', content)[1:]
        
        for bloque in bloques:
            try:
                lineas = bloque.strip().split('\n')
                info_line = lineas[0]
                url = lineas[1].strip()
                
                nombre_raw = info_line.split(',')[-1].strip()
                # Limpiar nombre para TMDB y para que el cliente vea algo bonito
                nombre_cliente = re.sub(r'\[.*?\]|\(.*?\)|\d{3,4}p|HD|FULL|4K|\.mp4|\.mkv', '', nombre_raw).strip()
                
                cat_match = re.search(r'group-title="([^"]+)"', info_line)
                categoria = cat_match.group(1) if cat_match else "VARIOS 🌐"
                
                logo = "https://i.imgur.com/8N3S3X8.png"
                
                # Si es VOD/Cine, forzamos TMDB
                if any(x in categoria.upper() for x in ["CINE", "NETFLIX", "HBO", "SERIES", "VOD", "ESTRENOS"]):
                    t_logo = buscar_en_tmdb(nombre_cliente)
                    if t_logo: logo = t_logo
                else:
                    # Si es TV, intentamos mantener el logo original
                    l_match = re.search(r'tvg-logo="([^"]+)"', info_line)
                    if l_match: logo = l_match.group(1)

                # REESCRIBIMOS LA LÍNEA M3U CON EL LOGO PARA SMARTERS
                nueva_linea = f'#EXTINF:-1 tvg-logo="{logo}" group-title="{categoria}",{nombre_cliente}'
                canales_m3u.append(f"{nueva_linea}\n{url}\n")
            except: continue

    with open(GLOBAL_M3U_FINAL, "w", encoding="utf-8") as f:
        f.writelines(canales_m3u)
    
    print(f"[✅] M3U reconstruido con {len(canales_m3u)-1} canales y logos incrustados.")

if __name__ == "__main__":
    generar_todo()
