import requests
import os
import json

def limpiar_y_cargar_json(texto):
    lineas = texto.split('\n')
    lineas_limpias = [l for l in lineas if not l.strip().startswith('//')]
    return json.loads('\n'.join(lineas_limpias))

def extraer_todo(url_base):
    headers = {'User-Agent': 'Mozilla/5.0'}
    base_stream = f"{url_base}:9000"
    archivos_fuente = ["XC.json", "jsm.json", "tvbox.json"]
    
    output_file = os.path.expanduser("~/iptv/listas_raw/shodan_vod_completo.m3u")
    
    print("="*40)
    print("🚀 BUSCANDO PELÍCULAS, SERIES Y ANIME...")
    print("="*40)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        total_encontrado = 0

        for fuente in archivos_fuente:
            try:
                r = requests.get(f"{base_stream}/{fuente}", headers=headers, timeout=10)
                if r.status_code != 200: continue
                
                data = limpiar_y_cargar_json(r.text)
                
                # Buscamos en todas las ramas del JSON (Recursivo simple)
                items_a_procesar = []
                if isinstance(data, dict):
                    # Xtream UI suele separar por 'movies', 'series', 'live'
                    for llave in ['movies', 'series', 'vod', 'anime', 'novelas', 'groups']:
                        if llave in data:
                            content = data[llave]
                            if isinstance(content, list): items_a_procesar.extend(content)
                elif isinstance(data, list):
                    items_a_procesar = data

                for item in items_a_procesar:
                    # Buscamos el nombre y la URL
                    name = item.get("name") or item.get("title")
                    u = item.get("url") or item.get("file") or item.get("link")
                    
                    # Identificar categoría para organizar
                    cat = "VOD_GENERAL"
                    n_lower = name.lower() if name else ""
                    if "serie" in n_lower: cat = "SERIES"
                    elif "anime" in n_lower: cat = "ANIME"
                    elif "novela" in n_lower: cat = "NOVELAS"
                    elif u and ("/movie/" in u or "/vod/" in u): cat = "PELICULAS"

                    if name and u:
                        f.write(f'#EXTINF:-1 group-title="SHODAN_{cat}",{name}\n')
                        final_url = u if u.startswith("http") else f"{base_stream}/{u}"
                        f.write(f'{final_url}\n')
                        total_encontrado += 1
            except:
                continue

        print(f"\n[✔] ¡PROCESO TERMINADO!")
        print(f"[*] Contenido total encontrado: {total_encontrado}")
        print(f"[*] Guardado en: listas_raw/shodan_vod_completo.m3u")

if __name__ == "__main__":
    extraer_todo("http://64.23.147.53")
