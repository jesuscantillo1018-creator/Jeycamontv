import os
import subprocess
import re
import requests
import shutil
from datetime import datetime

# --- CONFIGURACIÓN ---
os.environ['OPENSSL_CONF'] = os.path.expanduser('~/UnibanProject/openssl_legacy.cnf')
BASE_DIR = os.path.expanduser("~/iptv")
TOOLS = os.path.join(BASE_DIR, "tools")
LISTAS_RAW = os.path.join(BASE_DIR, "listas_raw")
GLOBAL_M3U = os.path.join(BASE_DIR, "global_jeycamon.m3u")

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

def main():
    print("\n" + "="*50)
    print("💎 JEYCAMON SUITE V6.5 - EL PANEL MAESTRO")
    print("="*50)

    # 1. MODO ASPIRADORA (PREGUNTA)
    opcion = input("\n[❓] ¿Quieres ingresar una nueva URL/Link RAW para limpiar? (s/n): ").lower()
    if opcion == 's':
        url_externa = input("[🔗] Pega el link M3U o tu link RAW de GitHub: ")
        try:
            r = requests.get(url_externa, headers=headers, timeout=15)
            if r.status_code == 200:
                with open(os.path.join(LISTAS_RAW, "importacion_limpieza.m3u"), "w", encoding="utf-8") as f:
                    f.write(r.text)
                print("[✅] Lista importada con éxito.")
        except:
            print("[!] No se pudo descargar la lista externa.")

    # 2. EJECUTAR RADAR LATAM
    print("\n[*] Ejecutando Radar Latam (vod_injector.py)...")
    subprocess.run(f"python3 {os.path.join(TOOLS, 'vod_injector.py')}", shell=True)

    # 3. CONSOLIDAR Y PROCESAR (ESTO LLAMA AL CONSTRUCTOR CON TMDB)
    print("\n[🛡️] Iniciando Auditoría y Clasificación Profesional...")
    # Forzamos la unión de todo lo que hay en listas_raw
    subprocess.run(f"cat {LISTAS_RAW}/*.m3u > {GLOBAL_M3U}_temp", shell=True)
    
    # Llamamos al constructor que ya tiene TMDB y estética Pro
    subprocess.run(f"python3 {os.path.join(BASE_DIR, 'core/constructor_json.py')}", shell=True)

    # 4. SUBIDA TOTAL A GITHUB
    print("\n" + "-"*30)
    subir = input("[📤] ¿Subir TODO a GitHub Maestro (incluyendo archivos nuevos)? (s/n): ").lower()
    if subir == 's':
        print("[🚀] Sincronizando repositorio...")
        os.chdir(BASE_DIR)
        subprocess.run("git add .", shell=True) # El punto agrega TODO, incluso archivos nuevos
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
        subprocess.run(f'git commit -m "Panel Pro Update: {fecha}"', shell=True)
        subprocess.run("git push origin maestro", shell=True)
        print("\n[✅] ¡LISTA ACTUALIZADA EN GITHUB!")

if __name__ == "__main__":
    main()
