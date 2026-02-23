import os
import subprocess
import re
import requests
import shutil
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

# --- CONFIGURACIÓN DE TU REPO ---
os.environ['OPENSSL_CONF'] = os.path.expanduser('~/UnibanProject/openssl_legacy.cnf')
BASE_DIR = os.path.expanduser("~/iptv")
TOOLS = os.path.join(BASE_DIR, "tools")
LISTAS_RAW = os.path.join(BASE_DIR, "listas_raw")
GLOBAL_M3U = os.path.join(BASE_DIR, "global_jeycamon.m3u")
CLASIFICADAS_DIR = os.path.join(BASE_DIR, "listas_clasificadas")
# TU LINK RAW OFICIAL
URL_GITHUB_RAW = "https://raw.githubusercontent.com/jesuscantillo1018-creator/Jeycamontv/maestro/global_jeycamon.m3u"

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

def check_link(url):
    try:
        r = requests.head(url, headers=headers, timeout=5, allow_redirects=True)
        return url if r.status_code == 200 else None
    except:
        return None

def sincronizar_y_reparar():
    print(f"\n[📡] CONECTANDO CON GITHUB: {URL_GITHUB_RAW}")
    
    # 1. Obtener la lista actual de tu GitHub
    try:
        res = requests.get(URL_GITHUB_RAW, timeout=10)
        github_content = res.text.splitlines()
    except:
        print("[!] Error: No se pudo leer tu GitHub. Verifica internet.")
        return 0

    # 2. Correr Radar para buscar links frescos
    print("[🔎] Ejecutando Radar de búsqueda...")
    subprocess.run(f"python3 {os.path.join(TOOLS, 'vod_injector.py')}", shell=True)
    
    # 3. Mapear canales encontrados por el radar
    nuevos_links = {} # { "Nombre del Canal": "URL_NUEVA" }
    temp_file = os.path.join(LISTAS_RAW, "estrenos_vod.m3u")
    if os.path.exists(temp_file):
        with open(temp_file, "r") as f:
            lines = f.readlines()
            for i in range(len(lines)):
                if lines[i].startswith("#EXTINF"):
                    name = lines[i].split(",")[-1].strip().upper()
                    if i+1 < len(lines):
                        nuevos_links[name] = lines[i+1].strip()

    # 4. Auditoría Inteligente
    print("[🧠] Analizando canales caídos y buscando reemplazos...")
    lista_final = ["#EXTM3U\n"]
    reemplazados = 0
    vivos = 0
    
    # Preparar auditoría de lo que ya tienes en GitHub
    urls_gh = []
    metadata_gh = []
    for i in range(len(github_content)):
        if github_content[i].startswith("#EXTINF"):
            urls_gh.append(github_content[i+1].strip())
            metadata_gh.append(github_content[i])

    with ThreadPoolExecutor(max_workers=30) as executor:
        status_vivos = list(executor.map(check_link, urls_gh))

    # 5. Reconstrucción con lógica de reemplazo
    for i in range(len(urls_gh)):
        nombre_canal = metadata_gh[i].split(",")[-1].strip().upper()
        link_actual = urls_gh[i]
        
        # Si el link original está vivo, se queda
        if status_vivos[i]:
            lista_final.append(f"{metadata_gh[i]}\n{link_actual}\n")
            vivos += 1
        # Si está muerto, buscamos si el radar trajo uno con el mismo nombre
        elif nombre_canal in nuevos_links:
            link_nuevo = check_link(nuevos_links[nombre_canal])
            if link_nuevo:
                print(f"  [♻️] REPARADO: {nombre_canal}")
                lista_final.append(f"{metadata_gh[i]}\n{link_nuevo}\n")
                vivos += 1
                reemplazados += 1
        # Si no hay reemplazo, el canal se descarta para mantener la lista limpia

    # 6. Guardar y Clasificar
    if os.path.exists(CLASIFICADAS_DIR): shutil.rmtree(CLASIFICADAS_DIR)
    os.makedirs(CLASIFICADAS_DIR, exist_ok=True)
    
    with open(GLOBAL_M3U, "w") as f:
        f.writelines(lista_final)

    print(f"\n[📊] RESULTADOS:")
    print(f"  - Canales que seguían vivos: {vivos - reemplazados}")
    print(f"  - Canales REPARADOS (inyectados): {reemplazados}")
    print(f"  - Total funcional: {vivos}")
    return vivos

def main():
    print("\n" + "="*50)
    print("💎 JEYCAMON INTELLIGENCE v5.0 - GITHUB SYNC")
    print("="*50)
    
    total = sincronizar_y_reparar()
    
    if total > 0:
        print("\n[📁] Generando JSON y archivos por categoría...")
        subprocess.run(f"python3 {os.path.join(BASE_DIR, 'core/constructor_json.py')}", shell=True)
        
        confirmar = input("\n[☁️] ¿Subir estas reparaciones a GitHub? (s/n): ").lower()
        if confirmar == 's':
            subprocess.run("git add .", shell=True, cwd=BASE_DIR)
            subprocess.run(f'git commit -m "Auto-Reparación: {total} canales vivos"', shell=True, cwd=BASE_DIR)
            subprocess.run("git push origin maestro", shell=True, cwd=BASE_DIR)
            print("[🚀] ¡GitHub actualizado y reparado!")

if __name__ == "__main__":
    main()
