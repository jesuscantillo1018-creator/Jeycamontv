import os
import subprocess
import re
import requests
import shutil
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

# --- CONFIGURACIÓN DE ENTORNO ---
os.environ['OPENSSL_CONF'] = os.path.expanduser('~/UnibanProject/openssl_legacy.cnf')
BASE_DIR = os.path.expanduser("~/iptv")
TOOLS = os.path.join(BASE_DIR, "tools")
LISTAS_RAW = os.path.join(BASE_DIR, "listas_raw")
GLOBAL_M3U = os.path.join(BASE_DIR, "global_jeycamon.m3u")
CLASIFICADAS_DIR = os.path.join(BASE_DIR, "listas_clasificadas")

def check_link(url):
    try:
        r = requests.head(url, timeout=8, allow_redirects=True)
        return url if r.status_code == 200 else None
    except:
        return None

def limpiar_carpetas_antiguas():
    """Limpia la carpeta de categorías para no mezclar con procesos viejos."""
    if os.path.exists(CLASIFICADAS_DIR):
        shutil.rmtree(CLASIFICADAS_DIR)
    os.makedirs(CLASIFICADAS_DIR, exist_ok=True)

def guardar_por_categoria(categoria, infoliana, url):
    """Guarda el canal en su archivo m3u correspondiente."""
    # Limpiamos el nombre de la categoría para que sea un nombre de archivo válido
    nombre_archivo = re.sub(r'[^\w\-_\. ]', '_', categoria) + ".m3u"
    path = os.path.join(CLASIFICADAS_DIR, nombre_archivo)
    
    modo = "a" if os.path.exists(path) else "w"
    with open(path, modo, encoding="utf-8") as f:
        if modo == "w":
            f.write("#EXTM3U\n")
        f.write(f"{infoliana}\n{url}\n")

def analizar_limpiar_y_clasificar():
    if not os.path.exists(GLOBAL_M3U): return 0

    print("\n[🛡️] Iniciando Auditoría, Filtro Anti-Duplicados y Clasificación...")
    limpiar_carpetas_antiguas()

    with open(GLOBAL_M3U, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    valid_entries = ["#EXTM3U\n"]
    urls_to_check = []
    metadata = {}
    vistos = set()

    for i in range(len(lines)):
        if lines[i].startswith("#EXTINF"):
            url = lines[i+1].strip() if i+1 < len(lines) else None
            if url and url.startswith("http") and url not in vistos:
                urls_to_check.append(url)
                metadata[url] = lines[i]
                vistos.add(url)

    if not urls_to_check: return 0

    print(f"[*] Verificando {len(urls_to_check)} enlaces únicos...")
    with ThreadPoolExecutor(max_workers=30) as executor:
        results = list(executor.map(check_link, urls_to_check))

    vivos = 0
    for url in results:
        if url:
            info = metadata[url]
            valid_entries.append(info)
            valid_entries.append(url + "\n")
            vivos += 1
            
            # Extraer categoría para guardar por separado
            match = re.search(r'group-title="([^"]+)"', info)
            cat = match.group(1) if match else "SIN_CATEGORIA"
            guardar_por_categoria(cat, info.strip(), url)

    with open(GLOBAL_M3U, "w", encoding="utf-8") as f:
        f.writelines(valid_entries)
    
    print(f"\n[📁] ¡Listas organizadas en: {CLASIFICADAS_DIR}")
    return vivos

def agregar_proveedor_shodan():
    print("\n[🔎] ¿Nuevo proveedor de Shodan? (URL/IP o ENTER):")
    nuevo = input("> ").strip()
    if nuevo:
        path_shodan = os.path.join(LISTAS_RAW, "shodan_manual.m3u")
        os.makedirs(LISTAS_RAW, exist_ok=True)
        with open(path_shodan, "a") as f:
            if not nuevo.startswith("http"): nuevo = "http://" + nuevo
            f.write(f'#EXTINF:-1 group-title="SHODAN_NUEVO", Canal_Shodan\n{nuevo}\n')

def subir_a_github(vivos):
    print(f"\n[📊] Resultado: {vivos} vivos.")
    if input("\n[☁️] ¿Subir a GitHub? (s/n): ").lower() == 's':
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
        subprocess.run("git add .", shell=True, cwd=BASE_DIR)
        subprocess.run(f'git commit -m "IPTV Update: {vivos} canales - {fecha}"', shell=True, cwd=BASE_DIR)
        subprocess.run("git push origin main", shell=True, cwd=BASE_DIR)
        print("[🚀] GitHub actualizado.")

def main():
    print("\n🚀 SUITE JEYCAMON V3.2: MODO ORGANIZADOR")
    agregar_proveedor_shodan()
    
    for script in ["vod_injector.py", "mega_import.py"]:
        path = os.path.join(TOOLS, script)
        if os.path.exists(path):
            print(f"[*] Ejecutando: {script}...")
            subprocess.run(f"python3 {path}", shell=True)

    print("[*] Consolidando listas...")
    subprocess.run(f"cat {LISTAS_RAW}/*.m3u > {GLOBAL_M3U}", shell=True)

    total_vivos = analizar_limpiar_y_clasificar()
    
    path_constructor = os.path.join(BASE_DIR, "core/constructor_json.py")
    if os.path.exists(path_constructor):
        subprocess.run(f"python3 {path_constructor}", shell=True)

    subir_a_github(total_vivos)

if __name__ == "__main__":
    main()
